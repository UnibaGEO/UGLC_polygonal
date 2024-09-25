#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     BGS - National Landslide Database (British Geological Survey)
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import apply_affidability_calculator, date_format

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/10_BGS_native.csv", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('10_ETGFI_lookuptables.json', 'r', encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["10_ETGFI LOOKUP TABLES"]

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
df_NEW['ID'] = "CALC"
df_NEW['OLD DATASET'] = "National Landslide Database (British Geological Survey)"
df_NEW['OLD ID'] = df_OLD['LS_ID'].fillna('ND')
df_NEW['VERSION'] = str("Last update 2020")
df_NEW['COUNTRY'] = "United Kingdom"
df_NEW['ACCURACY'] = df_OLD['PLUS_OR_MI'].astype(int).fillna('-99999')
df_NEW['START DATE'] = df_OLD['FIRST_KN_1'].fillna("1678-01-01").apply(date_format)
df_NEW['END DATE'] = df_OLD['FIRST_KN_1'].fillna("2023-12-31").apply(date_format)
df_NEW['TYPE'] = "ND"
df_NEW['TRIGGER'] = "ND"
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = "report"
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"BGS - locality: {repr(row['LOCATION'])}, {repr(row['NAME'])} - description: ND ", axis=1)
df_NEW['LINK'] ="Source: ND"

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/10_BGS_converted.csv", sep=',', index=False, encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             10_BGS_native conversion: DONE                               ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
