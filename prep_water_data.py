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
    
#convert date and year columns to datetime
df['new_report_date'] = pd.to_datetime(df.report_date)
df['new_install_year'] = pd.to_datetime(df.install_year,format='%Y.0')

#make age of well feature.  This will return in days, which assumes install year starts on Jan 1.  We may want to 
#make more date features.
# also tree methods may have a better time with 3.2 years than 1018 days
# this returns 0 days and NaTs.  Fill NaT with 9999 in XGB

df['age_well']=df.new_report_date - df.new_install_year

#binary target.  When status is yes == 0, when no OR maybe == 1
df['status_binary']=np.where(df.status_id=='yes',0,1)

df.to_csv(OUTPUT_FILE, index=False)
