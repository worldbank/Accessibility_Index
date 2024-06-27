# import dpeendent libraries

import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import box

import rasterio
from rasterio.mask import mask
from rasterio.io import MemoryFile
from rasterio.transform import Affine

import scipy

# Define a function to generate all the necessary parameters for our raster outputs based on the extent of the input shapefile
# Also extracts a generator of (geom, speed) values we'll use to rasterize the actual speed values into pixels

def get_raster_params(vector,base_rast_raw,speed_column):
    
    bds = vector.geometry.total_bounds
    
    # height and width
    ht = int(bds[3] - bds[1])
    wth = int(bds[2] - bds[0])
    
    # initial transform based on raw raster (DatasetReader object) and input vector extent
    base_tform = base_rast_raw.transform
    src_tform = rasterio.transform.from_bounds(bds[0],bds[1],bds[2],bds[3],wth,ht)
    
    # Assuming your input rasters are in meters, this is the cell size *in meters* of the final desired output.
    scale_factor_x = (base_tform.a / src_tform.a)
    scale_factor_y = (base_tform.e / src_tform.e)
    
    # calculate index of base raster pixel at road raster origin point
    edge_idx = base_rast_raw.index(src_tform.c, src_tform.f)

    # extract the latitude/longitude at the Upper Left ('ul') edge of this base raster pixel, so we can align the rasters exactly. Necessary for doing math later.
    # keep the same transform as the input file since we're not moving anything
    
    orig_x, orig_y = rasterio.transform.xy(transform=base_tform,\
                                  rows=edge_idx[0],\
                                  cols=edge_idx[1],\
                                  offset='ul')

    # create a new transformation with the new, aligned origin point

    dst_tform = Affine(src_tform.a * scale_factor_x, src_tform.b, orig_x,
                           src_tform.d, src_tform.e * scale_factor_y, orig_y)

    # generator of vector shapes and values (speed)
    shapes = ((geom,speed) for geom, speed in zip(vector.geometry,vector[speed_column]))
    
    return bds, ht, wth, src_tform, dst_tform, shapes, scale_factor_x, scale_factor_y

# extract origin points from a raster

def extract_origins(src, src_tform):
    
    # calculate index of base raster pixel at road raster origin point
    edge_idx = src.index(src_tform.c, src_tform.f)
    
    # extract the latitude/longitude at the Upper Left ('ul') edge of this base raster pixel, so we can align the rasters exactly. Necessary for doing math later.
    # keep the same transform as the input file since we're not moving anything

    orig_x, orig_y = transform.xy(transform=src_tform,\
                                  rows=edge_idx[0],\
                                  cols=edge_idx[1],\
                                  offset='ul')
    
# Define a function to turn the prepared vector into an appropriately sized numpy array using the generator from `get_raster_params`

def rasterize_vector(vector):

    # Run the above function to get all the necessary inputs for rasterization: parameters + the vector generator
    
    bds, ht, wth, src_tform, dst_tform, shapes, scale_factor_x, scale_factor_y = get_raster_params(vector)
    
    # Code downsamples the code while rasterizing, saving us major headaches with resampling in memory.
    
    road_rast = features.rasterize(shapes,\
                  out_shape = (int(ht / scale_factor_y),\
                               int(wth / scale_factor_x)),\
                  transform=dst_tform,
                  all_touched=True,
                  dtype = np.float64)
    
    return road_rast

# Define a function to export the numpy array to a GeoTIFF for spatial analysis / visualization purposes

def export_rast(vector, fin_rast):

    # calculate naming variables
    
    sn = vector.SN.item()
    district = vector.District.item()
    season = re.findall(r'(.*?)_speed',speed_column)[0]
    
    speed_out_name = os.path.basename(f'{sn}_{district}_{speed_column}.tif')
    fric_out_name = os.path.basename(f'{sn}_{district}_{season}_friction.tif')
    
    # Must re-run this to get correct parameters for the profile creation
    bds, ht, wth, src_tform, dst_tform, shapes, scale_factor_x, scale_factor_y = get_raster_params(vector)

    # Create metadata, including transformation, for the export
    fin_profile = {
        "driver": "GTiff",
        "dtype": "float32",
        "crs": {'init': dest_crs},
        "height": int(ht / scale_factor_y),
        "width": int(wth / scale_factor_x),
        "count": 1,
        "nodata": 0,
        "transform": dst_tform,
        "compress": 'LZW'
    }
    
    # compute friction surface
    fric_fin_rast = (1 / fin_rast) / (1000 / dst_tform.a)
    fric_fin_rast = fric_fin_rast.astype(np.float32)
    
    # Export speed raster
    with rasterio.open(
        os.path.join(data_dir,speed_dir,f'{res}',speed_out_name), 'w',**fin_profile) as dst:
        dst.write(fin_rast, indexes=1)
        
    # Export friction raster
    with rasterio.open(
        os.path.join(data_dir,fric_dir,f'proposed_roads//{res}//raw',fric_out_name), 'w',**fin_profile) as dst:
        dst.write(fric_fin_rast, indexes=1)


# Lightly adapted from https://gis.stackexchange.com/questions/290030/what-does-it-mean-to-reproject-a-satellite-image-from-utm-zone-13n-to-wgs84

def reproject_tif(source_file, destination_file,dest_crs):
    """Re-projects tif at source file to destination CRS at destination file.

    Args:
        source_file: file to re-project
        destination_file: file to store re-projection

    Returns:
        destination_file: where the re-projected file is saved at
    """

    with rasterio.open(source_file) as src:
        dst_crs = dest_crs
        transform, width, height = calculate_default_transform(
            src.crs,
            dst_crs,
            src.width,
            src.height,
            *src.bounds
        )

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height,
            "compress":'LZW'
        })

        with rasterio.open(destination_file, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest,
                    num_threads=-1
                )

        return destination_file



# for cutting down arrays where rasterio's masking routine adds an extra (null) row

def reference_slicer(a, b):
    index = [slice(0, dim) for dim in b.shape]
    for i in range(len(b.shape), len(a.shape)):
        index.append(slice(0,a.shape[i]))
    return a[tuple(index)]


# calculate the extent of the differences between two rasters gneerated using the same methods + parameters, but different data inputs
def dif_clip_calc(arr1,arr2,tform,dest_crs):
    
    dif = np.subtract(arr1, arr2).astype('float32')
    
    (y_index, x_index) = np.nonzero(dif > 0.001)
    x_coords, y_coords = tform * (x_index,y_index) # note change of x, y positions

    if x_coords.size > 0 and y_coords.size > 0 :
        # 30 subtraction \\ addition enlarges the bounding box slightly to include any half-cells
        minX = min(x_coords) - tform.a
        minY = min(y_coords) - tform.a
        maxX = max(x_coords) + tform.a
        maxY = max(y_coords) + tform.a

        # Generating bounding box coordinates for rasterio
        dif_clip_box = box(minX, minY, maxX, maxY) # make sure these are in the correct order!
        dif_clip_box_gdf = gpd.GeoDataFrame({'geometry': dif_clip_box}, index=[0], crs=({'init' : f'{dest_crs}'}))

        return dif, dif_clip_box, dif_clip_box_gdf
    else:
        return "Skip"

# for clipping in memory
def clip_in_memory(raw_rasterio_file,meta,clip_box,reference_img=None):

    with MemoryFile() as memfile:
        with memfile.open(**meta) as raw_in_mem:
            raw_in_mem.write(raw_rasterio_file,indexes=1)

            # Crop the memfile with the bounding box shape
            clip_in_mem, clip_in_mem_tform = mask(raw_in_mem, clip_box, crop=True, indexes=1)

            # sometimes rasterio mysteriously pads the mask  by 1 cell, despite instructions not to do so. If this is a problem, provide a reference image to manually cut it down to the correct size
            if reference_img is not None:

                clip_in_mem = reference_slicer(clip_in_mem,reference_img)

            return clip_in_mem, clip_in_mem_tform

        
# slope calculation code from here: https://github.com/dgketchum/dem/blob/master/dem.py

def get_slope(dem, mode='percent'):
    slope = scipy.ndimage.gaussian_gradient_magnitude(dem, 5, mode ='nearest')
    if mode == 'percent':
        pass
    if mode == 'fraction':
        slope = slope / 100
    if mode == 'degrees':
        slope = rad2deg(arctan(slope / 100))
    
    return slope
    