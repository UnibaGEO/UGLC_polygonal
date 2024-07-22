from dotenv import load_dotenv
import os
import geopandas as gpd
import pandas as pd

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# PALI -----------------------------------------------------------------------
# SHP to CSV
import geopandas as gpd

# Leggi il file SHP
df_orig = gpd.read_file(f"{root}/input/download/1_PALI_Patagonian Andes landslides inventory (poly)/Ground_Truth_database.shp")

# Assicurati che il CRS sia EPSG:4326
df_orig = df_orig.to_crs(epsg=4326)

# Genera il WKT_GEOM per i poligoni
df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)

# Save the GeoDataFrame as a CSV
df_orig.to_csv(f"{root}/input/download/01_PALI/Ground_Truth_database.csv", index=False)

#
# # COOLR_E-----------------------------------------------------------------------
# # SHP to CSV
# df_orig_e = gpd.read_file(f"{root}/input/download/01_COOLR/COOLR event points/nasa_coolr_events_point.shp")
# # Crete a GeoDataFrame using 'lon' and 'lat' columns for generating the WKT_GEOM
# gdf_orig_e = gpd.GeoDataFrame(df_orig_e,
#                              geometry=gpd.points_from_xy(df_orig_e['longitude'], df_orig_e['latitude']),
#                              crs='EPSG:4326')  # Set the CRS as EPSG:4326
# gdf_orig_e['WKT_GEOM'] = gdf_orig_e.geometry.apply(lambda geom: geom.wkt)
# # adding the missing 'injuries' and 'fatalities' columns
# gdf_orig_e['injuries']='-99999'
# gdf_orig_e['fatalities']='-99999'
#
# # Save the GeoDataFrame as a CSV
# gdf_orig_e.to_csv(f"{root}/input/download/01_COOLR/COOLR event points/nasa_coolr_events_point.csv", index=False)
#
# # COOLR MERGED -----------------------------------------------------------------------
#
# coolr_csv_e=pd.read_csv(f"{root}/input/download/01_COOLR/COOLR event points/nasa_coolr_events_point.csv",sep=',',encoding='UTF-8',low_memory=False)
# coolr_csv_r=pd.read_csv(f"{root}/input/download/01_COOLR/COOLR report points/nasa_coolr_reports_point.csv",sep=',',encoding='UTF-8',low_memory=False)
#
# # Set the OLD DATASET field
# coolr_csv_r['OLD DATASET'] = 'COOLR_R'
# coolr_csv_e['OLD DATASET'] = 'COOLR_E'
#
# # Merge the GeoDataFrames without duplicates (WKT_GEOM)
# coolr_csv_E_R = pd.concat([coolr_csv_r, coolr_csv_e], ignore_index=True)
# coolr_csv_E_R_filtered = coolr_csv_E_R.drop_duplicates(subset=['WKT_GEOM'])
# coolr_csv_E_R_filtered = coolr_csv_E_R_filtered.drop(columns=['geometry'])
#
# # Save the merged and filtered GeoDataFrame
# coolr_csv_E_R_filtered.to_csv(f"{root}/input/native_datasets/01_COOLR_native.csv",index=False)
#
