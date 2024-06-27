# Using these notebooks

*Step 1* reads the season-mode-service pixel data from the outputs from the notebooks in '4. Pop_Weighting' and aggregates these values within administrative units at the specified administrative levels. It also computes accessibility indices (normalised access time values) for each season-mode-service combination.

*Step 2* simply merges all the outputs from step 1 into complete csv's for each administrative level. The output columns are in order Admin data -> average travel time (column names ending in 'avg_adm(x)' -> accessibility index for each season-mode-service combination (column names ending in '_idx').  For the accessibility indices, values are between 0 and 1, with 1 meaning best accessibility.

*The accessibility indices can be used in additional analyses.  For example, if there are outputs for dry_season-multi_modal-universities and monsoon_season-multi_modal-universities, then year-round multi-modal accessibility to universities can be determined by weighting these columns together.  This will depend on your analysis requirements*

The notebooks are meant to be used in order. The notebooks are largely self explanatory by title, with the output of each feeding into the next. 
Run them in order, and ensure that the input files are prepared and located correctly - described below.

The notebooks have been simplified so that you only have to specify your project folder location in the notebooks' code.  In both notebooks, this is simply achieved by editing the line:

data_root = [your project folder]

For example, if your project folder is D:\github_accessibility, you will enter

data_root = 'D:\\github_accessibility\\'

This folder must correspond to the folder that was used when running the project_setup notebook (in 1. Data Prep folder).

Once all notebooks have been run, there will be files named 'adm(x)_mean_final.csv' and 'adm(x)_long_final.csv' (where x is each administrative level analysed, e.g. 2 or 3) in the folder [your project folder]\\access\\tables. The 'adm(x)_mean_final.csv' files contain, for each administrative unit, population-weighted average service access times for each season-service combination, and accessibility indices for all of these combinations (values between 0 and 1, with 1 meaning best accessibility). The 'adm(x)_long_final.csv' files contain, for each administrative unit, service access travel time bins with the percentage of each unit's population that lie within each bins, for each season-service combination.