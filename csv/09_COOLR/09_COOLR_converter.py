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

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/09_CA_native.csv", low_memory=False,encoding="utf-8")

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
df_NEW['OLD DATASET'] = "Colombia Landslides Dataset for the Capa Descargada area, Aristizábal E, Sánchez O. 2020"
df_NEW['OLD ID'] = df_OLD['id']
df_NEW['VERSION'] = str("updated to 2023")
df_NEW['COUNTRY'] = "Colombia"
df_NEW['ACCURACY'] = df_OLD['Incertidumb']
df_NEW['START DATE'] = pd.to_datetime(df_OLD['Fecha']).dt.strftime('%Y/%m/%d')
df_NEW['END DATE'] = pd.to_datetime(df_OLD['Fecha']).dt.strftime('%Y/%m/%d')
df_NEW['TYPE'] = df_OLD['TYPE']
df_NEW['TRIGGER'] = df_OLD['Detonante']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = "report"
df_NEW['FATALITIES'] = df_OLD['Fallecidos'].astype(int)
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row:f"CA - locality: Colombia,{row['Municipio']} ({row['Departament']}) - description: {row['Notas']} ", axis=1)
df_NEW['LINK'] = df_OLD.apply(lambda row:f"Source: {row['Fuente']}", axis=1)

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/09_CA_converted.csv", sep=',', index=False,encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             09_CA_native conversion: DONE                                ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
