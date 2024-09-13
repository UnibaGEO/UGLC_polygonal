from dotenv import load_dotenv
import os
import geopandas as gpd
import pandas as pd
import numpy as np

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Load the CSV
df_orig = pd.read_csv(f"{root}/input/download/06_PCLD/Canadian_landslide_database_Dec2023_version7.csv", sep=',', low_memory= False, encoding="utf-8")

df_orig['longitude'] = pd.to_numeric(df_orig['Longitude'], errors='coerce')
df_orig['latitude'] = pd.to_numeric(df_orig['Latitude'], errors='coerce')
df_orig = df_orig.dropna(subset=['latitude', 'longitude'])

# Crea un GeoDataFrame usando 'lon' e 'lat' colonne per generare il WKT_GEOM
gdf_orig = gpd.GeoDataFrame(df_orig,
                             geometry=gpd.points_from_xy(df_orig['longitude'], df_orig['latitude']),
                             crs='EPSG:4326')  # Set the CRS as EPSG:4326
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

# Standardizing Trigger Data
gdf_orig['Trigger'].fillna(gdf_orig['Contributor'], inplace=True)
gdf_orig['Trigger'] = gdf_orig['Trigger'].replace(' ', 'ND')
gdf_orig['Trigger'].fillna('ND', inplace=True)

# Standardizing Type Data
gdf_orig['Type'] = gdf_orig['Type'].fillna('ND')

# Creating  the DATAs and DATAf fields replacing the NaN with the oldest (except for pre 0000 dates) date and the most recent
gdf_orig['DATEs'] = (gdf_orig['Timing'].fillna('1677/12/31')).astype(str)
gdf_orig['DATEf'] = (gdf_orig['Timing'].fillna('2023/12/31')).astype(str)

# Merging the Name and Study area content, removing the NaN values
gdf_orig['Name'] = gdf_orig['Name'].fillna('ND')
gdf_orig['Study area'] = gdf_orig['Study area'].fillna('ND')
gdf_orig['Info'] = gdf_orig.apply(lambda row: f"{row['Study area']}, {row['Name']}", axis=1)

#standardize ACCURACY field content
gdf_orig['Accuracy'] = gdf_orig['Location confidence']
gdf_orig['Accuracy'] = gdf_orig.apply(lambda row: row['Reference'] if pd.isnull(row['Accuracy']) else row['Accuracy'], axis=1)
gdf_orig['Accuracy'] = gdf_orig['Accuracy'].fillna('30')

# Salva il GeoDataFrame come CSV
gdf_orig.to_csv(f"{root}/input/native_datasets/06_PCLD_native.csv", index=False)
