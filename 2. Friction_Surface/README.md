# Using these notebooks

These notebooks describe a process to create a custom friction surface for custom data inputs.  The concepts behind this friction surface modeling are documented in https://www.sciencedirect.com/science/article/abs/pii/S0966692321001101.

The notebooks are meant to be used in order. The notebooks are largely self explanatory by title, with the output of each feeding into the next. 
Run them in order, and ensure that the input files are prepared and located correctly - described below.

The notebooks have been simplified so that you only have to specify your project folder location in the notebooks' code.  In each of these four notebooks, this is simply achieved by editing the line:

data_root = [your project folder]

For example, if your project folder is D:\github_accessibility, you will enter

data_root = 'D:\\github_accessibility\\'

This folder must correspond to the folder that was used when running the project_setup notebook (in 1. Data Prep folder).

Once all notebooks have been run, there will be walking and multi-modal friction surfaces for your seasons in the folder [your project folder]\\friction

This process presupposes the following data inputs:
* OpenStreetMap roads vector data in shapefile format and with average slope per road segment added (using a tool such as ArcGIS Pro's Add Surface Information), and in UTM projection. Any filename will work as long as it is placed in the right folder (explained below)
* A raster Digital Elevation Model in tif format, any filename will work as long as it is placed in the right folder (explained below)
* A raster landcover model(s) in tif format - either a single landcover layer, or multiple landcover layers for different seasons.  For seasonal landcover the filename will be the season that each raster represents and copied to a specific folder (explained below).  For generic cover, any name will work as long as it is placed in the right folder (explained below)
* The raster files need to have the same extent, resolution, number of rows and columns, and projected to UTM (align rasters tool in QGIS can be used before projecting to UTM). For Pakistan, we use UTM 42N projection (EPSG:32642)
* Optionally, a rivers vector layer in shapefile format - can be WGS (4326) or UTM

==========
## DATA SETUP
==========

=============
### ROADS 
=============

- OpenStreetMap Roads can be downloaded for your area of interest from geofrabrik (https://download.geofabrik.de/) or using QGIS plugins like OSMDownloader or QuickOSM.  The code has been prepared to work with OSM roads data only, because of its predefined road classes that gets recategorised here.
  
- Your roads file must be in a .shp format (default when downloading from geofabrik).  It is a good idea to clip your roads data to your area of interest before running the notebooks, otherwise loading can take long.

- The slope of road segments need to be computed in order to categorise roads for default speed assignments.  This can be done in ArcGIS Pro using the Add Surface Information tool - there are tool in QGIS that can also do this, but we're used to the ArcGIS Pro method.  Ensure that your roads are projected to UTM before you run the tool!  Once completed, your dataset will have a 'Avg_Slope' field with slope values per road segment added to it.  This is also why it's a good idea to clip your roads to your area of interest, otherwise this step can take unnecessarily long.

- Once clipped and with slope added, copy your roads shapefile data in the folder [your project folder]\\inputs\\roads

- There are a number of parameter files, in .csv format, that need to be set before running the code.  These files are provided with the example input dataset and can be used as is, or adapted for your use case.  All these files need to be copied to the folder [your project folder]\\inputs\\roads
    - speeds.csv contains the default road speeds (in km/h) that will be used for roads based on the terrain type and road class combination
    - surface.csv contains the default road surface type that is assigned to the different road classes.  Options are "Paved", "Gravel", or "Earthen"
    - default_cond.csv contains the default road conditions that are assigned to roads based on the terrain type and road class combination. Options are "Good", "Fair", or "Poor".  The inputs here should reflect the general road conditions in your area of interest
    - finally, for each season there is a .csv file that contain road speed multipliers by which the road speeds from the speeds.csv file are multiplied, based on the road surface type and its condition.  Two example .csv files are included in the example data.  One for the dry season, dry.csv, and one for monsoon, msn.csv.  

- Once notebook Step 1 - Prepare Roads has completed, the final roads dataset with seasonal speeds will be saved in the folder [your project folder]\\inputs\\roads with the filename final_roads.gpkg.  The rest of the code will fetch this data from here automatically.

=================
### Elevation 
=================

- your elevation file needs to be in .tif format and copied to [your project folder]\\inputs\\elevation
- you elevation file needs to be aligned with your landcover files (same extent, resolution, number of rows and columns) and projected to UTM

=================
### Landcover 
=================

- if you are using seasonal landcover datasets, they need to be in .tif format with datatype int and copied to [your project folder]\\inputs\\landcover
- if you are using a single generic landcover dataset, it needs to be .tif format with datatype int and copied to [your project folder]\\inputs\\landcover\\Non_seasonal
- all landcover datasets must be aligned with the elevation file (same extent, resolution, number of rows and columns) and projected to UTM

- Regardless of whether you are using seasonal datasets or a generic landcover dataset, the file class_speed_modifers.csv (available in the example dataset) needs to be filled correctly and copied to the folder [your project folder]\\inputs\\landcover.
    - The classes and raster_values in the example .csv file correspond to the landcover datasets provided in example data (Google Dynamic World for seasonal, ESA for generic).
    - You need to verify that the landcover class values in your rasters correspond correctly to the raster_value in the .csv file
    - The names in the 'Class' column do not affect the model, and is purely for ease of interpretation.
    - If you are forcing rivers with additional waterways data, it is important to ensure that the class that represents water has 'yes' entered in the 'water' column of the.csv file.  This is important so that the same water speed divider is used for rivers as is used for water in the land cover datasets.
    - refer to "Spatial Analysis by Cost Functions" by Irmela Herzog (2020) for guidance on modifier values
  
- for each season that is investigated, regardless of using seasonal datasets or a generic dataset, there exists a .txt file that contains the seasonal speed modifier that is used to perform universal speed adjustments based on the general difficulty faced when travelling on foot in a specific season.  Example .txt files are provided in the example dataset for dry and monsoon seasons (dry.txt and msn.txt). These .txt files need to be copied to the folder [your project folder]\\inputs\\landcover
  
- For the season with the best walking conditions (dry here), this value would be 1 (no speed adjustment from base speeds).  For other seasons where walking on foot is more challenging (monsoon here), a value of less than 1 can be set, e.g. 0.8 for the monsoon season in the example data.  So, if you are walking at 5km/h on terrain classified as "bare" in the dry season, it will be adjusted to 5 * 0.8 = 4km/h in the monsoon season.

- IMPORTANT: if you are using seasonal landcover datasets, then the seasonal landcover dataset names need to be the same as the modifier txt file names, example dry.tif and dry.txt as in the example data.  If using generic landcover, the seasonal output names will correspond to the names in the .txt files.

==============
### Rivers
==============

- if you opt to force rivers into your landcover dataset, then a shapefile should be added to [your project folder]\\inputs\\water
- an example dataset is available in example data.

- ==============
### Administrative Boundaries 
==============

- You need to provide administrative boundaries for the levels that you are investigating.
- For example, if you are investigating accessibility up to adm3 level within a province (adm1), then you need to provide administrative boundaries for each level in the folders [your project folder]\\boundaries\\adm1, [your project folder]\\boundaries\\adm2, and [your project folder]\\boundaries\\adm3.
- These boundaries need to be in shapefile (.shp) format.