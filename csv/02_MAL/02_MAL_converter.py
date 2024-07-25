#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     GFLD - Global fatal landslide occurrence from 2004 to 2016, Froude, M. J. and Petley, D. N
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
df_OLD = pd.read_csv(f"{root}/input/native_datasets/02_GFLD_native.csv", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('02_GFLD_lookuptables.json', 'r', encoding='utf-8') as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["02_GFLD LOOKUP TABLES"]

# null values replacement in the Native Dataframe
df_OLD['Report_1'] = df_OLD['Report_1'].fillna('ND')
df_OLD['Location_M'] = df_OLD['Location_M'].fillna('ND')
df_OLD['Source_1'] = df_OLD['Source_1'].fillna('ND')

# Application of lookup Tables to the columns of the old DataFrame
for column in df_OLD.columns:
    lookup_table_key = f"{column}_lookup"  # Lookup table match-Key construction

    # Lookup Tables check if is a string or a dictionary
    if lookup_table_key in lookup_tables and isinstance(lookup_tables[lookup_table_key], dict):
        lookup_table = lookup_tables[lookup_table_key]

        # If the lookup table is marked as "ND" the sytem will keep the original content
        if lookup_table == "ND":
            continue
        else:
            # Update just the no-"ND" columns
            df_OLD[column] = df_OLD[column].map(lambda x: lookup_table.get(str(x), x))

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
df_NEW['OLD DATASET'] = "Global fatal landslide Catalog"
df_NEW['OLD ID'] = df_OLD['LandslideN']
df_NEW['VERSION'] = str("2017")
df_NEW['COUNTRY'] = df_OLD['Country']
df_NEW['ACCURACY'] = (np.sqrt(df_OLD['Precision'].astype(float) / np.pi)).apply(round).astype(int)
df_NEW['START DATE'] = df_OLD.apply(lambda row: pd.to_datetime(f"{row['Year']}/{row['Month']:02d}/{row['Day']:02d}", format='%Y/%m/%d').strftime('%Y/%m/%d'), axis=1)
df_NEW['END DATE'] = df_OLD.apply(lambda row: pd.to_datetime(f"{row['Year']}/{row['Month']:02d}/{row['Day']:02d}", format='%Y/%m/%d').strftime('%Y/%m/%d'), axis=1)
df_NEW['TYPE'] = "ND"
df_NEW['TRIGGER'] = df_OLD['Trigger'].fillna('ND')
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = "event"
df_NEW['FATALITIES'] = df_OLD['Fatalities'].fillna('-99999')
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"GFLD, locality: {repr(row['Location_M'])}, description: {repr(row['Report_1'])}", axis=1)
df_NEW['LINK'] = df_OLD.apply(lambda row: f"Source: {repr(row['Source_1'])}",axis=1)

# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/02_GFLD_converted.csv", index=False, encoding="utf-8")

print("________________________________________________________________________________________")
print("                             02_GFLD_native conversion: DONE                            ")
print("________________________________________________________________________________________")
#-----------------------------------------------------------------------------------------------------------------------

