import pandas as pd
import georasters as gr
import matplotlib.pyplot as plt
import os
import time

def process_pop_data(pop_file, country):
    """Takes a tif file for an individual country and converts it to a csv with the country name appended to every row"""
    start_time = time.time()
    pop_data = gr.from_file(pop_file)
    pop_df = pop_data.to_pandas()
    print("DataFrame created!")
    pop_df['value'] = pop_df['value'].apply(lambda x: round(x, 3))
    print("Total population of", country, ":", '{:,}'.format(pop_df['value'].sum())) #Sanity Check
    pop_df['lat'] = pop_df['y']
    pop_df['long'] = pop_df['x']
    print("Lat/Long Created!")
    pop_df['country'] = country
    print("Converting to CSV..")
    pop_df.to_csv(country + '_pop_data.csv', index_label = 'key')
    del pop_df #clear memory
    end_time = time.time()
    time_taken = round((end_time - start_time) / 60,1)
    print("Done!")
    print("Time taken:", time_taken, "minutes")
    
process_pop_data("India 100m Population/IND_ppp_2015_adj_v2.tif", "India")