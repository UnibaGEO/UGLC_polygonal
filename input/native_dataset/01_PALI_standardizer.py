from dotenv import load_dotenv
import os
import geopandas as gpd
import pandas as pd

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# PALI -----------------------------------------------------------------------
# SHP to CSV
import geopandas as gpd

# Leggi il file SHP
df_orig = gpd.read_file(f"{root}/input/download/1_PALI_Patagonian Andes landslides inventory (poly)/Ground_Truth_database.shp")

# Assicurati che il CRS sia EPSG:4326
df_orig = df_orig.to_crs(epsg=4326)

# Genera il WKT_GEOM per i poligoni
df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)
# Seleziona tutte le colonne tranne 'geometry'
columns_to_save = [col for col in df_orig.columns if col != 'geometry']

# Crea un nuovo DataFrame con le colonne selezionate
df_final = df_orig[columns_to_save]

# Salva il DataFrame come CSV
df_final.to_csv(f"{root}/input/native_dataset/01_PALI_native.csv", index=False)



