The Population directory contains 4 main categories of iPython notebooks.

The "WorldPop Data Parse" notebook takes tif files containing 2014 or 2015 population data for individual countries (from WorldPop) and converts them to CSVs.

The "[Country Name] Water and Population Parser" notebooks create water point data for each country (by filtering down the original water point data set), then add columns for the number of people within 1 km of each water point and for the number of total/functioning water points within 1 km of each water point. Each notebook outputs a csv containing that country's water point data.

The "Merge District Data" notebook takes the water point data for each country and appends district info for each water point. The first column added is broader, while the second is more specific (for instance, if the US were represented in the data, one column could be States and the second could be Counties). 

The "Water and Population Data to Postgres" Notebook takes the water point data for each country and creates tables with the same schema for each of them.    
