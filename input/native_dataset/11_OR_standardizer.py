import os
import geopandas as gpd
from dotenv import load_dotenv

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Load the shp
input_shapefile = f"{root}/input/download/11_NTMI/Landslide_Susceptibility_Map_Ireland/Landslide_Susceptibility_Map_Ireland/Landslide_Susceptibility_Map_Ireland/Individual_Files/Shapefiles/IE_GSI_LS_LOCATIONS_ITM.shp"
gdf = gpd.read_file(input_shapefile)

# Set the CRS to EPSG4326
crs_shapefile = gdf.crs
if crs_shapefile != 'EPSG:4326':
    gdf = gdf.to_crs(epsg=4326)

# Crete a GeoDataFrame using 'geometry' column for generating the WKT_GEOM
gdf['WKT_GEOM'] = gdf['geometry'].apply(lambda geom: f"POINT ({geom.xy[0][0]} {geom.xy[1][0]})")
gdf['TRIGGER'] = gdf.apply(lambda row: f"{row['TRIGGER_CA']if row['TRIGGER_CA'] is not None else 'ND'}, {row['TRIGGER__1'] if row['TRIGGER__1'] is not None else 'ND'}", axis=1)
gdf['SOURCE_MERGED'] = gdf.apply(lambda row: f"{row['REFERENCE_'] if row['REFERENCE_'] is not None else row['REFERENCE1'] if row['REFERENCE1'] is not None else 'ND'}", axis=1)
gdf['ACCURACY'] = gdf['ACCURACY'].astype(str)

# Save the GeoDataFrame as a CSV
output_csv = f"{root}/input/native_datasets/11_NTMI_native.csv"
gdf.to_csv(output_csv, index=False)