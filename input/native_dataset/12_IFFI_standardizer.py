import os
import geopandas as gpd
from dotenv import load_dotenv
import pandas as pd
from shapely import wkt


# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Lista dei file SHP da unire
shp_files = [f"{root}/input/download/17_IFFI/frane_piff_abruzzo_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_basilicata_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_bolzano_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_calabria_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_campania_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_emilia-romagna_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_friuli-venezia-giulia_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_lazio_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_liguria_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_lombardia_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_marche_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_molise_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_piemonte_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_puglia_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_sardegna_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_sicilia_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_toscana_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_trento_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_umbria_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_valle-d-aosta_opendata/frane_piff_opendataPoint.shp",
             f"{root}/input/download/17_IFFI/frane_piff_veneto_opendata/frane_piff_opendataPoint.shp",]


# Leggi il primo file SHP
merged_data = gpd.read_file(shp_files[0])

# Loop attraverso gli altri file e uniscili al primo
for shp_file in shp_files[1:]:
    data_to_merge = gpd.read_file(shp_file)
    merged_data = gpd.GeoDataFrame(
        pd.concat([merged_data, data_to_merge], ignore_index=True)
    )

# Salva il file unito
merged_data.to_file(f"{root}/input/download/17_IFFI/IFFI.shp")

# Load the shp
df_orig = gpd.read_file(f"{root}/input/download/17_IFFI/IFFI.shp")

# Set the CRS to EPSG4326
crs_shapefile = df_orig.crs
if crs_shapefile != 'EPSG:4326':
    df_orig = df_orig.to_crs(epsg=4326)

# Crete a GeoDataFrame using 'geometry' column for generating the WKT_GEOM
df_orig['WKT_GEOM'] = df_orig['geometry'].apply(lambda geom: f"POINT ({geom.xy[0][0]} {geom.xy[1][0]})")

# Save the GeoDataFrame as a CSV
df_orig.to_csv(f"{root}/input/native_datasets/17_IFFI_native.csv", index=False)
