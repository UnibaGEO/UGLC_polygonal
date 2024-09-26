#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     NTMI -  Landslide Inventory  (Irish Landslides Working Group - Geological Survey Ireland (GSI))
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import apply_affidability_calculator, populate_end_date, populate_start_date

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/11_NTMI_native.csv", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('11_OR_lookuptables.json', 'r', encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["11_OR LOOKUP TABLES"]

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

#NaN values filling
df_OLD['LOCATION_C'] = df_OLD['LOCATION_C'].fillna('ND')
df_OLD['EVENT_NAME'] = df_OLD['EVENT_NAME'].fillna('ND')
df_OLD['IMPACT_COM'] = df_OLD['IMPACT_COM'].fillna('ND')

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
df_NEW['OLD DATASET'] = "Landslide Inventory  (Irish Landslides Working Group - Geological Survey Ireland (GSI)"
df_NEW['OLD ID'] = df_OLD['EVENT_ID']
df_NEW['VERSION'] = str("Last update 2020")
df_NEW['COUNTRY'] = "Ireland"
df_NEW['ACCURACY'] = df_OLD['ACCURACY'].apply(lambda x: int(x) if pd.notna(x) else -99999)
df_NEW['START DATE'] = df_OLD.apply(populate_start_date, axis=1)
df_NEW['END DATE'] = df_OLD.apply(populate_end_date, axis=1)
df_NEW['TYPE'] = df_OLD['LANDSIDE_M']
df_NEW['TRIGGER'] = df_OLD['TRIGGER']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = df_OLD['TRIGGER'].apply(lambda x: 'report' if x == 'natural' else 'event')
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"NTMI - locality: {repr(row['LOCATION_C'])}, {repr(row['EVENT_NAME'])} - description: {repr(row['IMPACT_COM'])} ", axis=1)
df_NEW['LINK'] = df_OLD.apply(lambda row: f"Source: {repr(row['SOURCE_MERGED'])}", axis=1)

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/11_NTMI_converted.csv", sep=',', index=False, encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             11_NTMI_native conversion: DONE                              ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
