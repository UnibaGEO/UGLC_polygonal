#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     PCLD - Preliminary Canadian Landslide Database, Brideau Marc-Andre, Brayshaw Drew, Lipovsky Panya
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import date_f_correction, date_s_correction, apply_affidability_calculator

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/06_PCLD_native.csv", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('06_GEUS_DN_lookuptables.json', 'r', encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["06_GEUS_DN LOOKUP TABLES"]

# Application of lookup Tables to the columns of the old DataFrame
for column in df_OLD.columns:
    lookup_table_key = f"{column}_lookup"  # Lookup table match-Key construction

    # Lookup Tables check if is a string or a dictionary
    if lookup_table_key in lookup_tables and isinstance(lookup_tables[lookup_table_key], dict):
        lookup_table = lookup_tables[lookup_table_key]

        # If the lookup table is marked as "ND" the system will keep the original content
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
df_NEW['ID'] = "CALC"# range(1, len(df_OLD) + 1)
df_NEW['OLD DATASET'] = "Preliminary Canadian Landslide Database v.6.1 - Brideau et al. 2023"
df_NEW['OLD ID'] = df_OLD['LS_ID']
df_NEW['VERSION'] = str("V6.1")
df_NEW['COUNTRY'] = "Canada"
df_NEW['ACCURACY'] = df_OLD['Accuracy']
df_NEW['START DATE'] = df_OLD['DATEs'].apply(lambda x: pd.to_datetime(x, errors='coerce').strftime('%Y/%m/%d'))
df_NEW['END DATE'] = df_OLD['DATEf'].apply(lambda x: pd.to_datetime(x, errors='coerce').strftime('%Y/%m/%d'))
df_NEW['TYPE'] = df_OLD['Type']
df_NEW['TRIGGER'] = df_OLD['Trigger']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = df_OLD['Trigger'].apply(lambda x: 'report' if x == 'natural' else 'event')
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"PCLD - locality: Canada - description: {repr(row['Info'])}", axis=1)
df_NEW['LINK'] = df_OLD.apply(lambda row: f"Source: {row['Reference']}", axis=1)

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)


#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/06_PCLD_converted.csv", sep=',', index=False, encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             06_PCLD_native conversion: DONE                              ")
print("__________________________________________________________________________________________")
