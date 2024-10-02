import os
import geopandas as gpd
import zipfile
import pandas as pd
from dotenv import load_dotenv
import tempfile

# Enviroment loading from config.env file -----------------------------------------------------------------------
load_dotenv("../../config.env")
files_repo = os.getenv("FILES_REPO")
files_repo_linux = os.getenv("FILES_REPO_LINUX")

# Verify if there is a Windows G-Drive files repo or a Linux G-Drive files repo
if os.path.exists(files_repo):
    root = files_repo
else:
    root = files_repo_linux

print(f"Using root= {root}")

# -----------------------------------------------------------------------

# IFFI -----------------------------------------------------------------------
# SHP to CSV

# List to store dataframes
df_list = []

# Path to the folder containing the ZIP files
zip_folder = f"{root}/input/download/12_IFFI/"

# Iterate through all ZIP files matching the pattern
for filename in os.listdir(zip_folder):
    if filename.startswith("frane_poly_") and filename.endswith("_opendata.zip"):
        zip_path = os.path.join(zip_folder, filename)

        # Open the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Find all the components of the shapefile (.shp, .shx, .dbf, .prj)
            shapefile_members = [file for file in zip_ref.namelist() if file.endswith((".shp", ".shx", ".dbf", ".prj"))]

            # Create a temporary directory to extract the shapefile
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract all shapefile components into the temp directory
                zip_ref.extractall(temp_dir, shapefile_members)

                # Get the path of the extracted shapefile (.shp file)
                shapefile_path = os.path.join(temp_dir,
                                              [file for file in shapefile_members if file.endswith(".shp")][0])

                # Read the SHP file with all its associated components
                df_orig = gpd.read_file(shapefile_path)

                # Set the CRS as EPSG:4326
                df_orig = df_orig.to_crs(epsg=4326)

                # Generate the WKT_GEOM for the polygons
                df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)

                # Select all columns except for 'geometry'
                columns_to_save = [col for col in df_orig.columns if col != 'geometry']

                # Append the DataFrame to the list
                df_list.append(df_orig[columns_to_save])

# Concatenate all DataFrames
df_final = pd.concat(df_list, ignore_index=True)

# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/12_IFFI_native.csv"
df_final.to_csv(output_path, index=False, sep=';', encoding="utf-8")