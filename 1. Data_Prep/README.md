# Using these notebooks

This notebook describes the process to create the folder structure that will be required for easy loading of datasets in other notebooks.

Note that the code requires minor adaptations to setup your project correctly.

All the layers necessary to run the code are available in [Input](https://ucdavis.box.com/s/sni7hvtlgslee4gb4jj66p8886psurw9). Meanwhile, all results can be found in [Output](https://ucdavis.box.com/s/tmvf7k85ctp0g957nkp7fx1tqgbk6dx3).

The following variables are found in the notebook, and need to be adapted in the notebook for your project

==============================
## Project folder
==============================

1. First, you need to specify a project folder, example:

data_root = 'D:\\github_accessibility\\'

==============================
## Projection
==============================

2. Specify your projection system. Your input files will also have to be provided in the same projection.  For example, UTM 42N (Pakistan) is:

dest_crs = 'EPSG:32642'

dest_crs_id = '32642'

==============================
## Buffer distance
==============================

3. Set a buffer distance, in metres, around your desired area of interest (boundary).  Value can be set to 0 (no buffer) or larger.  It is important that the input datasets you provide (DEM, landcover, roads, destinations, etc.) extend beyond your boundary and buffer so that your selected area (with buffer) can be successfully clipped from the input data. Example, for a buffer of 2000 metres:

buffer_m = 2000

==============================
## Main administrative unit level / custom
==============================

3. Set your administrative unit (area of interest) extent. If your *largest* area is, for example, a province, select 'adm1'.  The division is set by commenting all lines of code for the levels, except for the one you are interested in.  It is also possible to provide your own, custom, area of interest, for which the "custom" line of code should be uncommented, and all others commented.  For example, if I want to analyse accessibility at provincial level (including districts and sub-districts later on), the largest administrative level is adm1, selected in the following manner:

\*NOTE: Currently, the code is not yet fully generic and is set up for adm2 and adm3 analyses within adm1 boundaries only... future versions will be more modular*

\# level = 'adm0'

level = 'adm1'

\# level = 'adm2'

\# level = 'adm3'

\# level = 'custom'

==============================
## Main administrative unit specifications
==============================

4. If you are not using a custom boundary and you are using a shapefile with various administrative unit names, you can select the one you are interested in by specifying its name, which should be obtained from the correct field in your shapefile.  If I am estimating accessibility at provincial level, then the name of the field in my dataset that contains all the province names is, for example, 'ADM1_EN' (as in the datasets that have been used here, and provided in example data).  The field name needs to be provided, for the notebook to find the correct shape, given the name of the unit you are investigating.  So, if I were to analyse the province "Khyber Pakhtunkhwa", the following values need to be set:

shapefile_adm_field = 'ADM1_EN'

adm_name = 'Khyber Pakhtunkhwa'

*NOTE: In future realeases, if you are performing an analysis with a custom boundary, these values won't matter and won't be used by the notebook and can be left as is.*

==============================
## Max administrative analysis depth
==============================

5. Select the maximum depth of administrative level that you are investigating.  For example, if you are investigating up to adm3 within a Province (adm1), then set max_level = 'adm3'

*NOTE: Currently, the code is not yet fully generic and is set up for either a max depth of adm2 or adm3 analyses within adm1 boundaries only. Future versions will be more modular. If adm3 is selected, adm2 stats will also be determined along with adm3.*

\# max_level = 'adm1' #for provinces

\# max_level = 'adm2' #for districts/regions

max_level = 'adm3' #for sub-districts/sub-regions (tehsils in Pakistan)

==============================
## Force rivers?
==============================

6. Seasonal land cover datasets already include water like rivers.  However, if you want to "force" waterways into your dataset, you can provide your own water dataset from a source like OSM (caution: some rivers are seasonal or mostly dry and do not truly create a barrier in accessibility to services, so forcing rivers could constrain the environment excessively).  If you want to force rivers, you set following value to 1 (yes), otherwise 0 (no), example:

force_rivers = 1

==============================
## Seasonal or generic land cover?
==============================

7. Finally, for land cover there are two options.  You can provide seasonal land cover datasets obtained for specific seasons from e.g. Google Dynamic World.  Alternatively, you can provide the traditional "single" land cover dataset that provides generalised land cover (e.g. ICIMOD, ESA WorldCover). Additional seasonal setups even when using a generalised land cover dataset are described in the README in the "2. Friction Surface" folder.  If you provide seasonal landcover datasets, you set value to 1 (yes) otherwise 0 (no), example:

seasonal_lc = 1

