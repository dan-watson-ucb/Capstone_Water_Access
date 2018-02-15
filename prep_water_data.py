import pandas as pd
import xgboost as xgb
import numpy as np
import sklearn as sk
from sklearn import model_selection
from sklearn.metrics import confusion_matrix, mean_squared_error
import os

#set input/output paths
#can eventually set this to the SOAPY API https://dev.socrata.com/foundry/data.waterpointdata.org/gihr-buz6
DATA_PATH = "~chandlermccann/Downloads/"
INPUT_FILE = os.path.join(DATA_PATH, "Water_Point_Data_Exchange_Complete_Dataset.csv")
OUTPUT_FILE = os.path.join(DATA_PATH, "cleaned_water_data.csv")

#read in the file
df = pd.read_csv(INPUT_FILE, encoding='latin-1')

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

def fill_missing(df):
    """args: pandas data frame that has already gone through prep_water_data.py
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
        
    return df

def make_well_years(df):
    if 'age_well_days' in df.columns and df.age_well_days.isnull().sum()==0:
        df['age_well_years'] = round(df.age_well_days/365,1)
    else:
        pass
    return df

#run the functions


df= fill_missing(df)

df = make_well_years(df)

#drop row ID
df.drop(['Row ID'], axis=1)

df.to_csv(OUTPUT_FILE, index=False)
