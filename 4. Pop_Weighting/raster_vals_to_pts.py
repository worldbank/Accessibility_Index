from typing import Union
import dask
from dask.highlevelgraph import HighLevelGraph
import dask.dataframe as dd
import dask.array as da
import xarray as xr
import pandas as pd
import numpy as np




def _add_pixel_values_to_df(
    pixels: np.ndarray,
    y_coords: np.ndarray,
    x_coords: np.ndarray,
    partition: pd.DataFrame,
    colname: str = "value",
) -> pd.DataFrame:
    # NOTE: coords must have already been chunked to align with `pixels`
    # FOR MAKSIM -- how do they get "already" chunked?
    arr = xr.DataArray(
        pixels, coords=[("y", y_coords.squeeze()), ("x", x_coords.squeeze())]
    )

    # Filter points that actually overlap with this chunk.
    # Besides improving performance, this also saves us from having to do any merge
    # step of the output dataframes: since raster chunks are non-overlapping
    # spatially, the contents of each dataframe will be non-overlapping as well.

    # minx, maxx, miny, maxy = x_coords[0], x_coords[-1], y_coords[-1], y_coords[0]
    minx, miny, maxx, maxy = (  # noqa: F841
        x_coords.min(),
        y_coords.min(),
        x_coords.max(),
        y_coords.max(),
    )

    inbounds_df = partition.query("@minx < x < @maxx and @miny < y < @maxy")
    points_xr = xr.Dataset.from_dataframe(inbounds_df[["x", "y"]])

    # Select pixel values at points
    # FOR MAKSIM -- so basically, we convert the points to an aligned raster dataset, select values that way, then return the values to a points dataset?
    pixel_values = arr.sel(x=points_xr.x, y=points_xr.y, method="nearest")
    pixel_values_df = pixel_values.reset_coords(drop=True).to_dataframe(name=colname)
    return pd.concat([inbounds_df, pixel_values_df], axis="columns")


def _pixel_values_at_points(
    arr: da.Array,
    ddf: dd.DataFrame,
    y_coords: da.Array,
    x_coords: da.Array,
    colname: str = "value",
) -> dd.DataFrame:
    # TODO this would be easy
    assert arr.ndim == 2, "Multi-band not supported yet"

    # Turn each chunk of the raster into a DataFrame of pixel values extracted from that chunk.
    px_values_df_chunks = arr.map_blocks(
        _add_pixel_values_to_df,
        # Expand coords arrays so they broadcast correctly
        y_coords[:, None],
        x_coords[None],
        ddf,
        colname=colname,
        # give a fake meta since `_add_pixel_values_to_df` would fail on dummy data
        meta=np.empty((0, 0)),
    )
    # NOTE: The cake is a lie! All of `px_values_df_chunks`'s metadata is wrong.
    # Its chunks are DataFrames, not ndarrays; its shape and dtype are also
    # not what `_meta` says.

    # To turn the "array" of DataFrames into one dask DataFrame, we have to flatten it
    # so its keys match the pattern of a DataFrame.
    # Sadly we can't just `.ravel()`, because that will add actual `np.reshape` tasks to the graph,
    # which will try to reshape the DataFrames (!!) to shapes that make no sense (!!!).

    # So we throw up our hands and write a dask graph by hand that just renames from one key to another.
    # TODO make this non-materialized (don't think it's blockwise-able though)

    df_name = f"pixel-values-{dask.base.tokenize(px_values_df_chunks)}"
    dsk = {
        (df_name, i): key
        for i, key in enumerate(dask.core.flatten(px_values_df_chunks.__dask_keys__()))
    }
    hlg = HighLevelGraph.from_collections(
        df_name, dsk, dependencies=[px_values_df_chunks]
    )

    meta = pd.concat(
        [ddf._meta, dd.utils.make_meta({colname: arr.dtype})], axis="columns"
    )
    return dd.DataFrame(hlg, df_name, meta, (None,) * len(dsk))


# example workflow
"""
Extract pixel values from a dask-backed DataArray/Dataset at x, y coordinates given in a dask DataFrame.

See the ``pixel_values_at_points`` docstring for usage.

Example
-------
>>> import dask
>>> import xarray as xr
>>> data = xr.DataArray(
...     da.random.random((256, 512), chunks=100),
...     coords=[("y", np.linspace(0, 1, 256)), ("x", np.linspace(0, 1, 512))],
... )
>>> df = dask.datasets.timeseries()
>>> df_with_values = pixel_values_at_points(data, df)
>>> df_with_values
Dask DataFrame Structure:
                   id    name        x        y pixel_values
npartitions=17
                int64  object  float64  float64      float64
                  ...     ...      ...      ...          ...
...               ...     ...      ...      ...          ...
                  ...     ...      ...      ...          ...
                  ...     ...      ...      ...          ...
Dask Name: pixel-values, 103 tasks
>>> df_with_values.head()
                       id    name         x         y  pixel_values
timestamp
2000-01-01 00:00:35   980     Tim  0.054010  0.108094      0.704963
2000-01-01 00:02:16  1045     Dan  0.009220  0.231619      0.904162
2000-01-01 00:05:04  1020  Ursula  0.116082  0.048629      0.463596
2000-01-01 00:06:31  1075  Ingrid  0.175014  0.383851      0.991749
2000-01-01 00:07:35  1017   Kevin  0.067010  0.149642      0.661196
"""

def pixel_values_at_points(
    raster: Union[xr.DataArray, xr.Dataset], points: dd.DataFrame
) -> dd.DataFrame:
    """
    Extract pixel values from a DataArray or Dataset at coordinates given by a dask DataFrame

    The ``points`` DataFrame should have columns ``x`` and ``y``, which should be in
    the same coordinate reference system as the ``x`` and ``y`` coordinates on the
    ``raster`` DataArray/Dataset.

    The output DataFrame will contain the same data as ``points``, with one column added
    per data variable in the Dataset (or just one column in the case of a DataArray).
    The column(s) will have the same names as the data variables.

    The output DataFrame will have one partition per chunk of the raster.
    Each partition will contain only the points overlapping that chunk.
    It will have the same index, but the divisions will be unknown.

    Note that the entire ``points`` DataFrame will be loaded into memory; it cannot
    be processed in parallel.
    """
    
    # Turn x and y coordinates into dask arrays, so we can re-create the xarray
    # object within our blockwise function. By using dask arrays instead of NumPy
    # array literals, dask will split up the coordinates into chunks that align with the pixels.
    # Ideally we could just use `DataArray.map_blocks` for all this, but 1) xarray's `map_blocks`
    # doesn't support auxiliary non-xarray collections yet (i.e. ``points```), and 2) it generates
    # a low-level graph instead of using a Blockwise layer.
    try:
        xs, ys = [
            da.from_array(
                raster.coords[coord].values,
                chunks=(
                    raster.chunks[raster.get_axis_num(coord)]
                    if isinstance(raster, xr.DataArray)
                    else raster.chunks[coord]
                    # ^ NOTE: raises error if chunks are inconsistent
                ),
                inline_array=True,
            )
            for coord in ["x", "y"]
        ]
    except KeyError as e:
        raise ValueError(f"`rasters` is missing the coordinate '{e}'")

    if isinstance(raster, xr.DataArray):
        return _pixel_values_at_points(
            raster.data, points, ys, xs, colname=raster.name or "value"
        )
    else:
        # TODO how do we merge all the DataFrames for non-overlapping arrays?
        # They might not even be the same length, partitions won't correspond, etc.
        # Ideally we'd have spatial partitioning to make the merge easy.
        # But even without, I guess we need the index on each DataFrame to actually
        # be identifying back to the original row so we can at least do a shuffle.
        if len(set(arr.shape for arr in raster.data_vars.values())) != 1:
            raise NotImplementedError(
                "Can't handle Datasets with variables of different shapes yet."
            )
        if len(set(arr.chunks for arr in raster.data_vars.values())) != 1:
            raise NotImplementedError(
                "Can't handle Datasets with variables of different chunk patterns yet."
            )

        # NOTE: we use the full points dataframe for the first raster, and just the xy-coords
        # for the subsequent ones, so we can concatenate all them column-wise without
        # duplicating data.
        points_justxy = points[["x", "y"]]
        dfs = [
            _pixel_values_at_points(
                arr.data, points if i == 0 else points_justxy, ys, xs, colname=name
            )
            for i, (name, arr) in enumerate(raster.data_vars.items())
        ]

        # NOTE: this is safe, since all the rasters have the same chunk pattern
        # (and so we assume are spatially aligned; should actually check this),
        # so the resulting DataFrames will have matching partitions.
        return dd.concat(dfs, axis="columns", ignore_unknown_divisions=True)