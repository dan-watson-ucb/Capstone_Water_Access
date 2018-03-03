import pandas as pd
import numpy as np
import os
import fuzzywuzzy
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

#set input/output paths
#can eventually set this to the SOAPY API https://dev.socrata.com/foundry/data.waterpointdata.org/gihr-buz6
DATA_PATH = "/Users/chandlermccann/Google Drive/Google Drive/Berkeley MIDS 2016/W210-Capstone_WaterProject"
INPUT_FILE = os.path.join(DATA_PATH, "Water_Point_Data_Exchange_Complete_Dataset.csv")
OUTPUT_FILE = os.path.join(DATA_PATH, "cleaned_water_data2.csv")

print("reading in input file from", INPUT_FILE)
#read in the file
df = pd.read_csv(INPUT_FILE, encoding='latin-1')

print("cleaning headings and creating features")
def clean_headings(df):
    #clean column names
    df.columns = [c.replace('#', '') for c in df.columns]
    return df

df=clean_headings(df)    

#convert date and year columns to datetime
df['new_report_date'] = pd.to_datetime(df.report_date)
df['new_install_year'] = pd.to_datetime(df.install_year,format='%Y.0')

#make age of well feature.  This will return in days, which assumes install year starts on Jan 1.  We may want to 
#make more date features.
# also tree methods may have a better time with 3.2 years than 1018 days
# this returns 0 days and NaTs.  Fill NaT with 9999 in XGB

df['age_well']=df.new_report_date - df.new_install_year

#ugly work around buy age_well comes out with hours, min and UTC.  Converting to string, splitting, and taking the days digits
df['age_well_days']=df.age_well.apply(lambda x: str(x).split()[0])

#binary target.  When status is yes == 0, when no OR maybe == 1
df['status_binary']=np.where(df.status_id=='yes',0,1)

#make a variable for time since last measurement
df['time_since_measurement'] = pd.to_datetime('today') - pd.to_datetime(df.new_report_date)

#convert it to years. It's a timedelta time stamp
df['time_since_meas_years']=df.time_since_measurement.apply(lambda x: round(x.days/365,1))

#Obscure missing values in water tech need to map 0, other ,to Missing
df.water_tech.replace({"0": "__MISSING__", " ": "__MISSING__","Other": "__MISSING__","None Other": "__MISSING__", "Unidentified":"__MISSING__" }, inplace=True)


def fill_missing(df):
    """args: pandas data frame
       returns: a pandas data frame that converted age_well_days """
    #this should really be in prep_water_data.py
    if 'age_well_days' in df.columns:
        df.replace(to_replace='NaT', value=99999, inplace=True) #have to replace the NaTs. Using a long value for missing years so tree picks up
        #convert to int since we dont want to label encode this
        df['age_well_days']= df['age_well_days'].astype(str).astype(int)
        
    #get columns that are of type object
    cols = df.select_dtypes(include=['object']).columns
    
    #fill with __MISSING___
    for col in cols:
        df[col].fillna('__MISSING__', inplace=True)
    
    #new_install_year not filling? hardcoding in now but should fix.  Something to do with forcing pd.Datetime to Y%?
    for annoying_col in ['install_year', 'new_install_year']:
        df[annoying_col].fillna('__MISSING__', inplace=True)
      
    return df


def make_well_years(df):
    if 'age_well_days' in df.columns and df.age_well_days.isnull().sum()==0:
        df['age_well_years'] = round(df.age_well_days/365,1)
    else:
        pass
    return df
    
#update the first function to return "no_match"
def fuzzymatch2(x, choices, scorer, cutoff):
    results = process.extractOne(
    x, choices=choices, scorer=scorer, score_cutoff= cutoff)
    if results is None:
        return "no match"
    else:
        return results[0]

#define fuzzy matching choices for water tech
choices_tech= ['Borehole', 'India Mark MK IMK II', 'Afridev', 'Gravity', 'Hand Pump','Electrical Pump', 'Bush Pump', 
          'Tube Well', 'Standpipe Stand Post', 'tap', 'Bucket','Indus', 'Pamir', 'Kardia', 'Kabul KABUL',
           'Spring River Stream Protected','Lake Pond Dam', 'municipal water supply', 'Rain Rainwater', 'Tank', 
          '__MISSING__', 'Well']
          
source_choices= ['Borehole', 'Tube Well', 'Well', 'Stand Post Tap','Hand Pump', 'Piped', 'Spring River Stream Protected', 
                 'Lake Pond Dam', 'Spring River Stream Unprotected',
                 'Sand','municipal water supply',  'Rain Rainwater', 'Tank',  '__MISSING__ Unknown']          

print("filling missing values....")         
#run the functions
df= fill_missing(df)

df = make_well_years(df)

print("executing fuzzy matching...")
#Execute fuzzy matching
df['fuzzy_water_source']= df.loc[:,'water_source'].apply(
                                            fuzzymatch2,
                                            args=(source_choices, 
                                                  fuzz.token_set_ratio, 
                                                 60)
)

df['fuzzy_water_tech']= df.loc[:,'water_tech'].apply(
                                            fuzzymatch2,
                                            args=(choices_tech, 
                                                  fuzz.token_set_ratio, 
                                                 60)
)
#drop row ID
df.drop(['Row ID'], axis=1, inplace = True)

#drop duplicates
df.drop_duplicates(inplace=True)

print("writing to csv to ", OUTPUT_FILE)
#write to csv
df.to_csv(OUTPUT_FILE, index=False)

print("DONE!")