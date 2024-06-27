# Using these notebooks

*Step 1* converts populated pixels in the population raster to separate datapoints, with its population size, coordinates, and its corresponding administrative unit(s).  This information is exported to csv, with a row for each pixel.

*Step 2* reads the population pixel data from the csv output from Step 1.  Then it determines each populated pixel's population weight within its corresponding administrative unit(s), extracts the service access times for each populated pixel, and then determines its population-weighted access times.  This is performed separately for each season-mode combination.

The notebooks are meant to be used in order. The notebooks are largely self explanatory by title, with the output of each feeding into the next. 
Run them in order, and ensure that the input files are prepared and located correctly - described below.

The notebooks have been simplified so that you only have to specify your project folder location in the notebooks' code.  In both notebooks, this is simply achieved by editing the line:

data_root = [your project folder]

For example, if your project folder is D:\github_accessibility, you will enter

data_root = 'D:\\github_accessibility\\'

This folder must correspond to the folder that was used when running the project_setup notebook (in 1. Data Prep folder).

Once all notebooks have been run, there will be a file named 'population_tabular_final.csv' in the folder [your project folder]\\inputs\\population, and multiple csv files in in the [your project folder]\\access_dir\\pixels. The csv files in the pixels folder contain each populated pixel's information, including population size, coordinates, adm data, population weight within its administrative unit(s), service access times, and population-weighted service access times.

*This process presupposes the following data inputs:*

- A Population data raster in tif format, any filename will work as long as it is placed in the right folder (explained below)

==========
## DATA SETUP
==========

=============
### POPULATION
=============

- your population file needs to be in .tif format and copied to [your project folder]\\inputs\\population
- *essential: this raster must be projected to UTM*
- while not essential, it is advised that your population file is aligned with your other input raster datasets used in the friction surface computations (same extent, resolution, number of rows and columns)