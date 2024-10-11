import pandas as pd
from shapely import wkt
import geopandas as gpd
from sklearn.neighbors import BallTree
from shapely.geometry import Point
from dotenv import load_dotenv
import os

# Enviroment loading from config.env file -----------------------------------------------------------------------

load_dotenv("../../config.env")
files_repo = os.getenv("FILES_REPO")
files_repo_linux = os.getenv("FILES_REPO_LINUX")

# Verify if its there is a Windows G-Drive files repo or a Linux G-Drive files repo
if os.path.exists(files_repo):
    root = files_repo
else:
    root = files_repo_linux

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------
#1 ASSIGN COUNTRY ( FROM NODATA, WITHOUT COLUMN)
file_path = f"{root}/lib/countries/countries.zip"

def assign_country_to_points(df):
    # Leggi i confini dei paesi dal file ZIP
    world = gpd.read_file("zip://" + file_path)

    # Crea un GeoDataFrame per i punti georeferenziati
    points = gpd.GeoDataFrame(df,
                              geometry=gpd.points_from_xy(df['long'], df['lat']),
                              crs='EPSG:4326')

    # Effettua un'operazione di "spazial join" per assegnare a ciascun punto il paese corrispondente
    points_with_country = gpd.sjoin(points, world[['geometry', 'NAME']], how='left', predicate='within')

    print("__________________________________________________________________________________________")
    print("                             COUNTRY Assignment: DONE                                     ")
    print("__________________________________________________________________________________________")

    return points_with_country

# -----------------------------------------------------------------------------------------------------------------------
#2 CORRECTION ND COUNTRY POINTS
def apply_country_corrections(df):
    """
    This function fixes all 'ND' value in the 'COUNTRY' column of the dataframe, using the Country name closest to the point coordinates.

    Input parameters:
    - df: pandas.DataFrame
        The dataframe contain all the geographic informations of the 'WKT_GEOM' and 'COUNTRY' columns.

    Returns:
    - pandas.Series
        A Pandas series wich contain the new fixed 'COUNTRY' column values.
    """
    # Convert the 'WKT_GEOM' column strings into point objects
    df['geometry'] = df['WKT_GEOM'].apply(wkt.loads).apply(Point)

    # Create a GeoDataFrame from df_NEW and specify 'geometry' as the geometry column
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Selects only points with value 'ND' in column 'COUNTRY'
    points_with_nd = gdf[gdf['COUNTRY'] == 'ND']

    # Select points without 'ND' to calculate distances
    points_without_nd = gdf[gdf['COUNTRY'] != 'ND']

    # Use BallTree to find the closest point for each point with 'ND'
    tree = BallTree(points_without_nd['geometry'].apply(lambda geom: (geom.x, geom.y)).tolist())
    distances, indices = tree.query(points_with_nd['geometry'].apply(lambda geom: (geom.x, geom.y)).tolist(), k=1)

    # Get the names of the correct states
    corrected_countries = gdf.loc[points_without_nd.index[indices.flatten()], 'COUNTRY'].values

    # Create a Pandas Series with the new corrected values
    corrected_series = pd.Series(corrected_countries, index=points_with_nd.index)

    # Assigns the new corrected values to the original dataframe
    df.loc[corrected_series.index, 'COUNTRY'] = corrected_series.values
    df.drop(columns=['geometry'], inplace=True)

    print("__________________________________________________________________________________________")
    print("                             COUNTRY Corrections: DONE                                  ")
    print("__________________________________________________________________________________________")

    return df['COUNTRY']

# -----------------------------------------------------------------------------------------------------------------------
#3 AFFIDABILITY CALCULATOR

def apply_RELIABILITY_calculator(df):
    # RELIABILITY function for assign a value between 1 and 10 into the RELIABILITY column
    def assign_RELIABILITY(row):
        accuracy = int(row['ACCURACY'])
        start_date = (row['START DATE'])
        end_date = (row['END DATE'])

        # accuracy NaN case
        if accuracy == -99999:
            return "10"
        # Out of range time case (1677/12/31)
        elif start_date == "1677/12/31":
            if 0 <= accuracy <= 100 and start_date == "1677/12/31":
                return "2"
            elif 100 < accuracy <= 250 and start_date == "1677/12/31":
                return "4"
            elif 250 < accuracy <= 500 and start_date == "1677/12/31":
                return "6"
            elif 500 < accuracy <= 1000 and start_date == "1677/12/31":
                return "8"
            elif accuracy > 1000 and start_date == "1677/12/31":
                return "9"
        # Normal dates case
        else:
            if 0 <= accuracy <= 100 and start_date == end_date:
                return "1"
            elif 0 <= accuracy <= 100 and start_date != end_date:
                return "2"
            elif 100 <= accuracy <= 250 and start_date == end_date:
                return "3"
            elif 100 <= accuracy <= 250 and start_date != end_date:
                return "4"
            elif 250 <= accuracy <= 500 and start_date == end_date:
                return "5"
            elif 250 <= accuracy <= 500 and start_date != end_date:
                return "6"
            elif 500 <= accuracy <= 1000 and start_date == end_date:
                return "7"
            elif 500 <= accuracy <= 1000 and start_date != end_date:
                return "8"
            elif accuracy > 1000 and start_date == end_date:
                return "9"
            elif accuracy > 1000 and start_date != end_date:
                return "9"
    print("__________________________________________________________________________________________")
    print("                             RELIABILITY  calculation: DONE                              ")
    print("__________________________________________________________________________________________")

    # Apply the RELIABILITY on it's column
    df['RELIABILITY'] = df.apply(assign_RELIABILITY, axis=1)
    return df

# -----------------------------------------------------------------------------------------------------------------------
# 4 - START DATE and END DATE calculator (only UTH)
# START DATE date composer
def populate_start_date(row):
    if row['d_h_move1'] != 0:
        return f"{int(row['d_h_move1'])}/01/01"
    elif row['d_h_move2'] != 0:
        return f"{int(row['d_h_move2'])}/01/01"
    elif row['d_h_move3'] != 0:
        return f"{int(row['d_h_move3'])}01/01"
    else:
        return "1937/01/01"

# END DATE date composer
def populate_end_date(row):
    if row['d_h_move3'] != 0:
        return f"{int(row['d_h_move3'])}/12/31"
    elif row['d_h_move2'] != 0:
        return f"{int(row['d_h_move2'])}/12/31"
    elif row['d_h_move1'] != 0:
        return f"{int(row['d_h_move1'])}/12/31"
    else:
        return "2012/12/31"

# -----------------------------------------------------------------------------------------------------------------------