from dotenv import load_dotenv
import os
import geopandas as gpd
import pandas as pd

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

# COOLR -----------------------------------------------------------------------
# SHP to CSV

# event polygons
# Read the SHP file
df_orig_e = gpd.read_file(f"{root}/input/download/9_Cooperative Open Online Landslide Repository (COOLR)\POLY\poly_nasa_coolr_events\\nasa_coolr_events_poly.shp", sep=';')

# Set the CRS as EPSG:4326
df_orig_e = df_orig_e.to_crs(epsg=4326)

# Generate the WKT_GEOM for the polygons
df_orig_e['WKT_GEOM'] = df_orig_e.geometry.apply(lambda geom: geom.wkt)
#df_orig_e[''].fillna('ND', inplace=True)
df_orig_e['RECORD TYPE'] = 'event'

# Select all columns except for 'geometry'
e_columns_to_save = [col for col in df_orig_e.columns if col != 'geometry']

# Create a new DataFrame with the selected columns
df_e_final = df_orig_e[e_columns_to_save]
# ------------------

# report polygons
# Read the SHP file
df_orig_r = gpd.read_file(f"{root}/input/download/9_Cooperative Open Online Landslide Repository (COOLR)\POLY\poly_nasa_global_landslide_catalog\\25.NASA Cooperative Open Online Landslide Repository (COOLR) Reports.shp", sep=';')

# Set the CRS as EPSG:4326
df_orig_r = df_orig_r.to_crs(epsg=4326)

# Generate the WKT_GEOM for the polygons
df_orig_r['WKT_GEOM'] = df_orig_r.geometry.apply(lambda geom: geom.wkt)
#df_orig_r[''].fillna('ND', inplace=True)
df_orig_r['RECORD TYPE'] = 'report'

# Select all columns except for 'geometry'
r_columns_to_save = [col for col in df_orig_r.columns if col != 'geometry']

# Create a new DataFrame with the selected columns
df_r_final = df_orig_r[r_columns_to_save]

# ------------------

# Merging the event and report catalog together
df_final = pd.concat([df_r_final, df_e_final], ignore_index=True)

# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/09_COOLR_native.csv"
df_final.to_csv(output_path, index=False, sep='|', encoding="utf-8")

### ------------------------------------------------------------