#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     MAL
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json
import numpy as np
from lib.function_collection import apply_affidability_calculator
from dotenv import load_dotenv
import os

# Enviroment loading from config.env file -----------------------------------------------------------------------

load_dotenv("../../config.env")
files_repo = os.getenv("FILES_REPO")
files_repo_linux = os.getenv("FILES_REPO_LINUX")

# Verify if its there is a Windows G-Drive files repo or a Linux G-Drive files repo
if os.path.exists(files_repo):
    root = files_repo
else:
    root = files_repo_linux

print(f"Using root= {root}")

# -----------------------------------------------------------------------

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_dataset/02_MAL_native.csv", low_memory=False, encoding="utf-8")

# New dataframe Configuration
new_data = {
    'WKT_GEOM': [],
    'NEW DATASET': [],
    'ID': [],
    'OLD DATASET': [],
    'OLD ID': [],
    'VERSION': [],
    'COUNTRY': [],
    'ACCURACY': [],
    'START DATE': [],
    'END DATE': [],
    'TYPE': [],
    'TRIGGER': [],
    'AFFIDABILITY': [],
    'RECORD TYPE': [],
    'FATALITIES': [],
    'INJURIES': [],
    'NOTES': [],
    'LINK': []
}

# New dataframe Creation
df_NEW = pd.DataFrame(new_data)

# New Dataframe Updating with the Old Dataframe columns content values
df_NEW['WKT_GEOM'] = df_OLD['WKT_GEOM']
df_NEW['NEW DATASET'] = "UGLC"
df_NEW['ID'] = "CALC" #range(1, len(df_OLD) + 1)
df_NEW['OLD DATASET'] = "Malesian Earthquake induced landslides"
df_NEW['OLD ID'] = df_OLD['Id']
df_NEW['VERSION'] = str("V1")
df_NEW['COUNTRY'] = "Malesia"
df_NEW['ACCURACY'] = "0"
df_NEW['START DATE'] = "2008/12/31"
df_NEW['END DATE'] = "2016/03/21"
df_NEW['TYPE'] = "ND"
df_NEW['TRIGGER'] = "seismic"
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = "event"
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"MAL, locality: Malesia, description: ND,area: {repr(row['area'])},perimeter: ND,volume: {repr(row['vol_xu'])}", axis=1)
df_NEW['LINK'] = "Source: ND"

# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/02_MAL_converted.csv", index=False, encoding="utf-8")

print("________________________________________________________________________________________")
print("                              02_MAL_native conversion: DONE                            ")
print("________________________________________________________________________________________")
#-----------------------------------------------------------------------------------------------------------------------

