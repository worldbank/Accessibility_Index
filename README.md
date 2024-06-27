# README

These folders contain simplified versions of notebooks that were used by the Poverty and Equity GP's spatial analysis support to investment projects and flooding analysis in Pakistan. These notebooks describe the various steps taken to determine access times to services.

While Poverty and Equity GP also consider govermental road data, these notebooks are made for general use using OSM roads data.  This is because government datasets that are usually integrated into roads data vary in structure and naming conventions, and it is thus difficult to write code that is generically compatible with these. Destination datasets can be provided from OSM or custom user-created, or other sources.  As long as the correct data preparation steps are followed.  The correct data preparation procedures are discussed in the README file located in the "2. Friction Surface" folder.

All the layers necessary to run the code are available in [Input](https://ucdavis.box.com/s/sni7hvtlgslee4gb4jj66p8886psurw9). Meanwhile, all results can be found in [Output](https://ucdavis.box.com/s/tmvf7k85ctp0g957nkp7fx1tqgbk6dx3).

## Repository structure

Code for this assignment was organized within Jupyter notebook as these are comfortable environments for geographers, data scientists, and increasingly economists to develop and test complex (spatial) analyses. 

The notebooks are organized in sub-folders by functionality under **notebooks**. Each folder contains a README stating any assumptions and need-to-know information for using the notebooks. The anticipated order of operations is:

1. Data Prep
2. Friction Surface
3. Access Modeling
4. Population Weighting
5. Aggregation

## Environment Setup

This work was done using python 3.8.10 on Anaconda instances running in a Windows virtual machine. We have enclosed a *requirements.txt* file listing all the python libraries referenced. We cannot guarantee these will work out of the box on UNIX or other systems; budget time accordingly.

Follow the instructions in the file "2024_Geospatial Anaconda Environment Setup_Workflow.txt" to set up your environment and to use jupyter notebooks.

## Reuse

Significant effort was expended to clean up and generalize the friction surface and access modeling notebooks. This was done with the expectation that these are the most complex, hard-to-repeat, and valuable components of the work. 

In all notebooks it is only necessary to edit a single line of code, to specify the location of the project's folder.  The project setup notebook will already set up all folders and filenames in this folder, and the required data can be copied to the correct folders and mostly do not need to have specific names, but correct file types and GIS preparation.

## Concepts

Reusing the work here will be hard even for experienced geographers without a firm understanding of the conceptual background. We recommend reading https://openknowledge.worldbank.org/handle/10986/35073 for details.
