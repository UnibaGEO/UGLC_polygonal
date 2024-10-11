#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     JLD - Japan landslide dataset for semantic segmentation
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import os
from dotenv import load_dotenv
from lib.function_collection import apply_RELIABILITY_calculator

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
df_OLD = pd.read_csv(f"{root}/input/native_dataset/08_JLD_native.csv", low_memory=False, sep=';', encoding="utf-8")

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
    'RELIABILITY': [],
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
df_NEW['ID'] = "CALC"
df_NEW['OLD DATASET'] = "Japan landslide dataset for semantic segmentation"
df_NEW['OLD ID'] = df_OLD['id']
df_NEW['VERSION'] = "V.1 - 29/04/2020"
df_NEW['COUNTRY'] = "Japan"
df_NEW['ACCURACY'] = str("0")
df_NEW['START DATE'] = df_OLD['START DATE']
df_NEW['END DATE'] = df_OLD['END DATE']
df_NEW['TYPE'] = "ND"
df_NEW['TRIGGER'] = "ND"
df_NEW['RELIABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = "event"
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_NEW.apply(lambda row: f"JLD - locality:{row['COUNTRY']}", axis=1) + df_OLD.apply(lambda row: f", description: ND, area: ND, perimeter: ND, volume: ND", axis=1)
df_NEW['LINK'] = "Source: ND"

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_RELIABILITY_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/08_JLD_converted.csv", sep=',', index=False, encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             08_JLD_native conversion: DONE                               ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
