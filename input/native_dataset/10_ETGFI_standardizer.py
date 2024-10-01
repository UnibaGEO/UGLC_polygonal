from dotenv import load_dotenv
import os
import geopandas as gpd

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

# ETGFI -----------------------------------------------------------------------
# SHP to CSV

# Read the SHP file
df_orig = gpd.read_file(f"{root}/input/download/10_Earthquake-Triggered Ground-Failure Inventories_POLY/26_ETGFI-POLY .shp")

# Set the CRS as EPSG:4326
df_orig = df_orig.to_crs(epsg=4326)

# null geometries cleaning
none_geometries = df_orig[df_orig.geometry.isna()]
df_orig = df_orig.dropna(subset=['geometry'])
print(f"{len(none_geometries)} null geometries removed from the file")

# Generate the WKT_GEOM for the polygons
df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)
df_orig['location'] = df_orig['event_name'].str.split(' - ', n=1).str[1]
df_orig['inventory_'].fillna('ND', inplace=True)
df_orig['comments'].fillna('ND', inplace=True)
df_orig['Shape_Leng'].fillna('ND', inplace=True)
df_orig['area'].fillna('ND', inplace=True)
df_orig['descriptio'].fillna('ND', inplace=True)
df_orig['source_lin'].fillna('ND', inplace=True)
df_orig['TYPE'] = df_orig['descriptio']

# Select all columns except for 'geometry'
columns_to_save = [col for col in df_orig.columns if col != 'geometry']

# Create a new DataFrame with the selected columns
df_final = df_orig[columns_to_save]

# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/10_ETGFI_native.csv"
df_final.to_csv(output_path, index=False, sep=';', encoding="utf-8")
