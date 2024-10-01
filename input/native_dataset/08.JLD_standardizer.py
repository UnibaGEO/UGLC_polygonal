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

# JLD -----------------------------------------------------------------------
# SHP to CSV

# Read the SHP file
shape_numbers = [0, 2, 4, 5, 6, 7, 8, 10, 12, 14, 15, 16, 21, 30, 32]

# Listing all the shapefile dataframes
df_list = []

for n in shape_numbers:
    file_path = f"{root}/input/download/8_GIAPPONE/3775870/SHAPEFILES_LANDSLIDES/vetor_landslide/landslide_{n}.shp"
    if os.path.exists(file_path):
        df_temp = gpd.read_file(file_path)
        df_temp['id'] = f"LS_{n}"  # Add the number of the native shape as native ID
        df_list.append(df_temp)
    else:
        file_path = f"{root}/input/download/8_GIAPPONE/3775870/SHAPEFILES_LANDSLIDES/vetor_landslide/landslides_{n}.shp"
        df_temp = gpd.read_file(file_path)
        df_temp['id'] = f"LS_{n}"  # Add the number of the native shape as native ID
        df_list.append(df_temp)

# Unisci tutti i DataFrame in un unico GeoDataFrame
df_orig = gpd.GeoDataFrame(pd.concat(df_list, ignore_index=True))

# Set the CRS as EPSG:4326
df_orig = df_orig.to_crs(epsg=4326)

# Generate the WKT_GEOM for the polygons
df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)

# Select all columns except for 'geometry'
columns_to_save = [col for col in df_orig.columns if col != 'geometry']

# Create a new DataFrame with the selected columns
df_final = df_orig[columns_to_save]

# Add 'START DATE' and 'END DATE' columns
df_final['START DATE'] = '1677/12/31'
df_final['END DATE'] = '2020/12/31'

# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/08_JLD_native.csv"
df_final.to_csv(output_path, index=False, sep=';', encoding="utf-8")

### ------------------------------------------------------------

