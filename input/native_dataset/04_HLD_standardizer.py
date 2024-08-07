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

# HLD -----------------------------------------------------------------------
# SHP to CSV

# Read the SHP file
df_orig = gpd.read_file(f"{root}/input/download/4_HAITI/haiti_landslides_2021/haiti_landslides_2021/2021_landslides.shp")


# Set the CRS as EPSG:4326
df_orig = df_orig.to_crs(epsg=4326)


# Generate the WKT_GEOM for the polygons
df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)


# Select all columns except for 'geometry'
columns_to_save = [col for col in df_orig.columns if col != 'geometry']


# Create a new DataFrame with the selected columns
df_final = df_orig[columns_to_save]


# Add 'START DATE' and 'END DATE' columns
df_final['START DATE'] = '14/08/2021'
df_final['END DATE'] = '31/12/2021'


# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/04_HLD_native.csv"
df_final.to_csv(output_path, index=False, encoding="utf-8")

### ------------------------------------------------------------

