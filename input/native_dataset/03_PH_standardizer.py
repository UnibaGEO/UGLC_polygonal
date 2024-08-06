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
df_final1['START DATE'] = '01/10/2019'
df_final1['END DATE'] = '31/10/2019'
df_final2['START DATE'] = '01/11/2019'
df_final2['END DATE'] = '30/11/2019'
df_final3['START DATE'] = '01/12/2019'
df_final3['END DATE'] = '31/12/2019'

# Concatenate the DataFrames
df_final = pd.concat([df_final1, df_final2, df_final3])

# Save the final DataFrame to a CSV file
output_path = f"{root}/input/native_dataset/03_PH_native.csv"
df_final.to_csv(output_path, index=False, encoding="utf-8")

### ------------------------------------------------------------

#from shapely import wkt

# Load the final CSV file back into a DataFrame
#df_final = pd.read_csv(output_path)

# Convert WKT_GEOM to geometries
#df_final['geometry'] = df_final['WKT_GEOM'].apply(wkt.loads)

# Create a GeoDataFrame
#gdf = gpd.GeoDataFrame(df_final, geometry='geometry', crs="EPSG:4326")

# Sort by 'START DATE' to give priority to earlier dates
#gdf = gdf.sort_values('START DATE')

# Create an empty GeoDataFrame to store the final non-overlapping polygons
#gdf_non_overlapping = gpd.GeoDataFrame(columns=gdf.columns, crs=gdf.crs)

# Iterate through each polygon and add it to the final GeoDataFrame if it doesn't overlap with existing ones
#for idx, row in gdf.iterrows():
    # Check for overlaps
#    if not gdf_non_overlapping.intersects(row.geometry).any():
#        gdf_non_overlapping = gdf_non_overlapping._append(row)

# Drop the old geometry column and rename the new one
#gdf_non_overlapping = gdf_non_overlapping.drop(columns='geometry')
#gdf_non_overlapping = gdf_non_overlapping.rename(columns={'geometry': 'WKT_GEOM'})

# Save the final non-overlapping DataFrame to a new CSV file
#output_path_non_overlapping = f"{root}/input/native_dataset/03_PH_native_non_overlapping.csv"
#gdf_non_overlapping.to_csv(output_path_non_overlapping, index=False, encoding="utf-8")

