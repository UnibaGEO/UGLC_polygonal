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

# UTH -----------------------------------------------------------------------
# SHP to CSV

# Read the SHP file
df_orig = gpd.read_file(f"{root}/input/download/7_UTAH/LandslideInventoryPolygons_-126329647010983062/LandslideInventoryPolygons.shp")

# Set the CRS as EPSG:4326
df_orig = df_orig.to_crs(epsg=4326)

# Generate the WKT_GEOM for the polygons
df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)
df_orig['d_name'].fillna('ND', inplace=True)
df_orig['d_thicknes'].fillna('unknown', inplace=True)
df_orig['confidence'].fillna('Low', inplace=True)
df_orig['comments'].fillna(' ', inplace=True)
df_orig['activity'].fillna('unknown', inplace=True)

# Select all columns except for 'geometry'
columns_to_save = [col for col in df_orig.columns if col != 'geometry']

# Create a new DataFrame with the selected columns
df_final = df_orig[columns_to_save]

# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/07_UTH_native.csv"
df_final.to_csv(output_path, index=False, sep='|', encoding="utf-8")

### ------------------------------------------------------------

