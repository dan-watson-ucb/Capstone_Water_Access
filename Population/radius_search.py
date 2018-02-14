#import packages
import pandas as pd
from geoindex import GeoGridIndex, GeoPoint
import dask.dataframe as dd
from dask.multiprocessing import get

#Load Swaziland Population File
swaz_pop = pd.read_csv("swaz_pop_data.csv")

#Load Water Data
water_data = pd.read_csv("Water_Point_Data_Exchange_Complete_Dataset.csv")

#Create df with only Swaziland water
swaz_water = water_data[water_data['#country_name'] == 'Swaziland']

#Create Geo Index of Swaziland Population Data
geo_index = GeoGridIndex()
for index, row in swaz_pop.iterrows():
    geo_index.add_point(GeoPoint(row['y'], row['x'], ref=row['value']))
    
#Calculate population with x distance of random well
def calculate_population_within_x_km(row, index, km):
    center_point = GeoPoint(row['#lat_deg'], row['#lon_deg'])
    total_population = 0
    try:
        for point,distance in index.get_nearest_points(center_point, km, 'km'):
            total_population += point.ref
    except:
        print("Invalid data - Record skipped")
    #print("Total population within", km, "kilometers:", int(total_population))
    return total_population

#Add 1 km radius population data to each well
tqdm.pandas()
swaz_water['1 km population'] = swaz_water.progress_apply(lambda row: calculate_population_within_x_km(row, geo_index, 1),
                                                  axis = 1)

#Create new csv
swaz_water.to_csv("Swaziland_Water_w_Population.csv")
