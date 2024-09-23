#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     CA - Colombia Landslides Dataset for the Capa Descargada area, Aristizábal E, Sánchez O. 2020
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import apply_affidability_calculator

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
df_OLD = pd.read_csv(f"{root}/input/native_dataset/09_COOLR_native.csv", sep="|", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('09_COOLR_lookuptables.json', 'r', encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["09_COOLR LOOKUP TABLES"]

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
df_NEW['ID'] = "CALC"
df_NEW['OLD DATASET'] = "Cooperative Open Online Landslide Repository (NASA) - report and event polygons"
df_NEW['OLD ID'] = df_OLD['ev_id']
df_NEW['VERSION'] = str("2019")
df_NEW['COUNTRY'] = df_OLD['ctry_name'] #DA CONTROLLARE CON LOOKUP TABLE
df_NEW['ACCURACY'] = df_OLD['loc_acc'].fillna('-99999', inplace=True) #DA CONTROLLARE CON LOOKUP TABLE
df_NEW['START DATE'] = df_OLD['ev_date'].combine_first(df_OLD['START DATE']) #DA CONTROLLARE CON LOOKUP TABLE
df_NEW['END DATE'] = df_OLD['ev_date'].combine_first(df_OLD['END DATE']) #DA CONTROLLARE CON LOOKUP TABLE
df_NEW['TYPE'] = df_OLD['ls_cat'] #DA CONTROLLARE CON LOOKUP TABLE
df_NEW['TRIGGER'] = df_OLD['ls_trig'] #DA CONTROLLARE CON LOOKUP TABLE
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = df_OLD['RECORD TYPE']
df_NEW['FATALITIES'] = df_OLD['fatalities'] #DA CONTROLLARE CON LOOKUP TABLE
df_NEW['INJURIES'] = df_OLD['injuries'] #DA CONTROLLARE CON LOOKUP TABLE
#DA CONTROLLARE CON LOOKUP TABLE
df_NEW['NOTES'] = df_NEW.apply(lambda row: f"COOLR - locality:{row['COUNTRY']}", axis=1) + df_OLD.apply(lambda row: f", description: {row['ev_title']} {row['ev_desc']}, area: {row['shape_Area']}, perimeter: {row['shape_Leng']}, volume: ND", axis=1)
#DA CONTROLLARE CON LOOKUP TABLE
df_NEW['LINK'] = df_OLD.apply(lambda row:f"Source: {row['src_name']} - {row['src_link']}", axis=1)

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/09_COOLR_converted.csv", sep=',', index=False, encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             09_COOLR_native conversion: DONE                             ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
