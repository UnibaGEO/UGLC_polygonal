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

# PH -----------------------------------------------------------------------
# SHP to CSV

# Read the SHP file
## October file
df_orig1 = gpd.read_file(f"{root}/input/download/3_PHILIPPINE/7520726/landslides_ott2019.shp")
## November file
df_orig2 = gpd.read_file(f"{root}/input/download/3_PHILIPPINE/7520726/landslides_nov2019.shp")
## December file
df_orig3 = gpd.read_file(f"{root}/input/download/3_PHILIPPINE/7520726/landslides_dic2019.shp")


# Set the CRS as EPSG:4326
df_orig1 = df_orig1.to_crs(epsg=4326)
df_orig2 = df_orig2.to_crs(epsg=4326)
df_orig3 = df_orig3.to_crs(epsg=4326)

# Generate the WKT_GEOM for the polygons
df_orig1['WKT_GEOM'] = df_orig1.geometry.apply(lambda geom: geom.wkt)
df_orig2['WKT_GEOM'] = df_orig2.geometry.apply(lambda geom: geom.wkt)
df_orig3['WKT_GEOM'] = df_orig3.geometry.apply(lambda geom: geom.wkt)

# Select all columns except for 'geometry'
columns_to_save1 = [col for col in df_orig1.columns if col != 'geometry']
columns_to_save2 = [col for col in df_orig2.columns if col != 'geometry']
columns_to_save3 = [col for col in df_orig3.columns if col != 'geometry']

# Create a new DataFrame with the selected columns
df_final1 = df_orig1[columns_to_save1]
df_final2 = df_orig2[columns_to_save2]
df_final3 = df_orig3[columns_to_save3]

# Add 'START DATE' and 'END DATE' columns
df_final1['START DATE'] = '2019/10/01'
df_final1['END DATE'] = '2019/10/31'
df_final2['START DATE'] = '2019/11/01'
df_final2['END DATE'] = '2019/11/31'
df_final3['START DATE'] = '2019/12/01'
df_final3['END DATE'] = '2019/12/31'

# Concatenate the DataFrames
df_final = pd.concat([df_final1, df_final2, df_final3])

# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/03_PH_native.csv"
df_final.to_csv(output_path, index=False, encoding="utf-8")


