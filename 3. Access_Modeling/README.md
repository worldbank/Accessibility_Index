# Using these notebooks

Step 1 uses the friction surface(s) previously generated and destinations to batch create access surfaces, one for each destination for each travel scenario (season-mode).

The notebooks have been simplified so that you only have to specify your project folder location in the notebooks' code.  
In this notebook, this is simply achieved by editing the line:

data_root = [your project folder]

For example, if your project folder is D:\github_accessibility, you will enter

data_root = 'D:\\github_accessibility\\'

This folder must correspond to the folder that was used when running the project_setup notebook (in 1. Data Prep folder).

=========
## Inputs
=========
The inputs to this notebook are the friction surfaces located in the folder [project folder]\\friction, and the destination files.  By default, for each season there will be walking and multimodal friction surfaces in the folder.  If you are only interested in one of these modes, simply remove the friction surfaces of the modes you are not interested in from the folder.  This will avoid unnecessary computation which can take long if your area is large and if you have many destination files.

*Your destination files need to be projected to UTM (EPSG:32642 for Pakistan) and .gpkg format.  The filenames should indicate the service locations that they contain.*

*Your destination files need to be placed in [project folder]\\inputs\\destinations*

In the example dataset, two destination files are provided.  They are already projected and in the right format.  The locations in these two files were obtained using QuickOSM in QGIS.  Nevertheless, you can create your own destination files from any source, as long as they are projected and in .gpkg format.