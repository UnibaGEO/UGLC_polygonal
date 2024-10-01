import os
import geopandas as gpd
from dotenv import load_dotenv

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


# OR -----------------------------------------------------------------------
# SHP to CSV

# Read the SHP file
df_orig = gpd.read_file(f"{root}/input/download/11_OREGON/landslide_OR.shp")

# Set the CRS as EPSG:4326
df_orig = df_orig.to_crs(epsg=4326)

# Generate the WKT_GEOM for the polygons
df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)

# General data fixes
df_orig['CONFIDENCE'].fillna('-99999', inplace=True)
df_orig['START DATE'] = df_orig['DATE_MOVE']
df_orig['START DATE'].fillna(df_orig['AGE'], inplace=True)
df_orig['START DATE'].fillna('1677/12/31', inplace=True)
df_orig['END DATE'] = df_orig['DATE_MOVE']
df_orig['END DATE'].fillna(df_orig['AGE'], inplace=True)
df_orig['END DATE'].fillna('2021/07/30', inplace=True)
df_orig['TYPE_MOVE'].fillna('ND', inplace=True)
df_orig['Descrip'].fillna('ND', inplace=True)
df_orig['AREA'].fillna('ND', inplace=True)
df_orig['VOL'].fillna('ND', inplace=True)
df_orig['DEEP_SHAL'].fillna('ND', inplace=True)
df_orig['SHAPE_Leng'].fillna('ND', inplace=True)

# Select all columns except for 'geometry'
columns_to_save = [col for col in df_orig.columns if col != 'geometry']

# Create a new DataFrame with the selected columns
df_final = df_orig[columns_to_save]

# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/11_OR_native.csv"
df_final.to_csv(output_path, index=False, sep=';', encoding="utf-8")
