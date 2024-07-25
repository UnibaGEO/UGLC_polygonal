#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC_POLY DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     PALI
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import json
from lib.function_collection import apply_country_corrections,apply_affidability_calculator
import pandas as pd
import os
from dotenv import load_dotenv
from shapely import wkt

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
df_OLD = pd.read_csv(f"{root}/input/native_dataset/01_PALI_native.csv", low_memory=False, encoding="utf-8")


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
df_NEW['ID'] = "CALC"  #range(1, len(df_OLD) + 1)
df_NEW['OLD DATASET'] = "Patagonian Andes Landslides Inventory"
df_NEW['OLD ID'] = "ND"
df_NEW['VERSION'] = str("2022")
df_NEW['COUNTRY'] = str("Patagonia")
df_NEW['ACCURACY'] = "0"
df_NEW['START DATE'] = '2020/01/01'
df_NEW['END DATE'] = '2021/12/31'
df_NEW['TYPE'] = 'ND'
df_NEW['TRIGGER'] = 'ND'
df_NEW['AFFIDABILITY'] = 'CALC'
df_NEW['RECORD TYPE'] = 'event'
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"PALI, locality: Patagonia, description: ND,area: {repr(row['AREA'])},perimeter:{repr(row['PERIMETER'])},volume: ND", axis=1)
df_NEW['LINK'] = "ND"
#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------


apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/01_PALI_converted.csv", index=False, encoding="utf-8")

print("________________________________________________________________________________________")
print("                             01_PALI_native conversion: DONE                           ")
print("________________________________________________________________________________________")

#-----------------------------------------------------------------------------------------------------------------------
# End
#-----------------------------------------------------------------------------------------------------------------------