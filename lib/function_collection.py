import pandas as pd
from shapely import wkt
import geopandas as gpd
from sklearn.neighbors import BallTree
from shapely.geometry import Point
from dotenv import load_dotenv
import os
import calendar

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

def apply_affidability_calculator(df):
    # Affidability function for assign a value between 1 and 10 into the AFFIDABILITY column
    def assign_affidability(row):
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
    print("                             AFFIDABILITY  calculation: DONE                              ")
    print("__________________________________________________________________________________________")

    # Apply the affidability on it's column
    df['AFFIDABILITY'] = df.apply(assign_affidability, axis=1)
    return df

# -----------------------------------------------------------------------------------------------------------------------
#4 START_DATE CORRECTION

def trasforma_data_start(data):

    # Conversione da yyyy/d/mm a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%Y/%d/%m').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da mm/d/yyyy a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da mm/d/yyyy,Periodo a yyyy/mm/d
    try:
        # Splitta la data e il periodo
        parti = data.split(',')
        data_senza_periodo = parti[0]

        # Converte la data nel formato desiderato
        nuova_data = datetime.strptime(data_senza_periodo, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da mm/yyyy a yyyy/mm
    try:
        nuova_data = datetime.strptime(data, '%m/%Y').strftime('%Y/%m/01')
        return nuova_data
    except ValueError:
        pass
        # Conversione da yyyy/mm a yyyy/mm
    try:
        nuova_data = datetime.strptime(data, '%Y/%m').strftime('%Y/%m/01')
        return nuova_data
    except ValueError:
        pass

    #Conversione da d1/m1/y1-d2/m2/y2 a y1/m1/d1

    try:
        data_inizio, data_fine = data.split('-')
        data_inizio = datetime.strptime(data_inizio.strip(), '%m/%d/%y').strftime('%Y/%m/%d')
        return data_inizio


    except ValueError:
        pass

    # Conversione da yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data, '%Y').strftime('%Y/01/01')
        return nuova_data
    except ValueError:
        pass

    # Conversione da yyyy/mm/d1-d2 a yyyy/mm/d1
    try:
        data_inizio, _ = data.split('-')
        data_inizio = datetime.strptime(data_inizio.strip(), '%Y/%m/%d').strftime('%Y/%m/%d')
        return data_inizio
    except ValueError:
        pass

    # Conversione da -yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data[1:], '%Y').strftime('%Y/01/01')
        return nuova_data
    except ValueError:
        pass

    # Conversione da -mm/d/yyyy h:m:s AM/PM in yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M:%S %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da -mm/d/yyyy h:m AM/PM in yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da abbreviazione mese/anno a YYYY/MM/01
    try:
        nuova_data = datetime.strptime(data, '%b.%Y').strftime('%Y/%m/01')
        return nuova_data
    except ValueError:
        pass
        # Conversione da y1y1y1y1-y2y2y2y2 a y1y1y1y1/01/01
        try:
            y1, y2 = data[:4], data[4:]
            nuova_data = f"{y1}/01/01"
            return nuova_data
        except ValueError:
            pass
    # Conversione da mm/d/yyyy,Giorno settimana a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y, %A').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Se non viene effettuata nessuna trasformazione, restituisci la data originale

    print("__________________________________________________________________________________________")
    print("                             START DATE  correction: DONE                                 ")
    print("__________________________________________________________________________________________")

    return data

# -----------------------------------------------------------------------------------------------------------------------
#5 END DATE CORRECTION

from datetime import datetime

def trasforma_data_end(data):

    # Conversione da yyyy/d/mm a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%Y/%d/%m').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da mm/d/yyyy a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da mm/d/yyyy,Periodo a yyyy/mm/d
    try:
        # Splitta la data e il periodo
        parti = data.split(',')
        data_senza_periodo = parti[0]

        # Converte la data nel formato desiderato
        nuova_data = datetime.strptime(data_senza_periodo, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    #Conversione da mm/yyyy a yyyy/mm/dd

    try:
        nuova_data = datetime.strptime(data, '%m/%Y')
        if nuova_data.month == 2:
            nuovo_giorno = 28
        elif nuova_data.month == 1:
            nuovo_giorno = 31
        elif nuova_data.month == 3:
            nuovo_giorno = 31
        elif nuova_data.month == 4:
            nuovo_giorno = 30
        elif nuova_data.month == 5:
            nuovo_giorno = 31
        elif nuova_data.month == 6:
            nuovo_giorno = 30
        elif nuova_data.month == 7:
            nuovo_giorno = 31
        elif nuova_data.month == 8:
            nuovo_giorno = 31
        elif nuova_data.month == 9:
            nuovo_giorno = 30
        elif nuova_data.month == 10:
            nuovo_giorno = 31
        elif nuova_data.month == 11:
            nuovo_giorno = 30
        elif nuova_data.month == 12:
            nuovo_giorno = 31

        nuova_data = nuova_data.replace(day=nuovo_giorno).strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    #Conversione da yyyy/mm a yyyy/mm/dd
    try:
        nuova_data = datetime.strptime(data, '%Y/%m')
        if nuova_data.month == 2:
            nuovo_giorno = 28
        elif nuova_data.month == 1:
            nuovo_giorno = 31
        elif nuova_data.month == 3:
            nuovo_giorno = 31
        elif nuova_data.month == 4:
            nuovo_giorno = 30
        elif nuova_data.month == 5:
            nuovo_giorno = 31
        elif nuova_data.month == 6:
            nuovo_giorno = 30
        elif nuova_data.month == 7:
            nuovo_giorno = 31
        elif nuova_data.month == 8:
            nuovo_giorno = 31
        elif nuova_data.month == 9:
            nuovo_giorno = 30
        elif nuova_data.month == 10:
            nuovo_giorno = 31
        elif nuova_data.month == 11:
            nuovo_giorno = 30
        elif nuova_data.month == 12:
            nuovo_giorno = 31

        nuova_data = nuova_data.replace(day=nuovo_giorno).strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    #Conversione da d1/m1/y1-d2/m2/y2 a y1/m1/d1

    try:
        data_inizio, data_fine = data.split('-')
        data_fine = datetime.strptime(data_fine.strip(), '%m/%d/%y').strftime('%Y/%m/%d')
        return data_fine
    except ValueError:
        pass

    # Conversione da yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data, '%Y').strftime('%Y/12/31')
        return nuova_data
    except ValueError:
        pass

    # Conversione da yyyy/mm/d1-d2 a yyyy/mm/d1
    try:
        _,data_fine, _ = data.split('-')
        data_fine = datetime.strptime(data_fine.strip(), '%Y/%m/%d').strftime('%Y/%m/%d')
        return data_fine
    except ValueError:
        pass

    # Conversione da yyyy/mm/d a yyyy/mm/d ----------------------------
    try:
        nuova_data = datetime.strptime(data, '%Y/%m/%d').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da -yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data[1:], '%Y').strftime('%Y/12/31')
        return nuova_data
    except ValueError:
        pass

    # Conversione da -mm/d/yyyy h:m:s AM/PM in yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M:%S %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da -mm/d/yyyy h:m AM/PM in yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

# Conversione da y1y1y1y1-y2y2y2y2 a y1y1y1y1/01/01
    try:
        y1, y2 = data[:4], data[4:]
        nuova_data = f"{y1}/12/31"
        return nuova_data
    except ValueError:
        pass
    # Conversione da mm/d/yyyy,Giorno settimana a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y, %A').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Se non viene effettuata nessuna trasformazione, restituisci la data originale
    print("__________________________________________________________________________________________")
    print("                             END DATE  correction: DONE                                   ")
    print("__________________________________________________________________________________________")

    return data

# ----------------------------------------------------------------------------------------------------------------------
#6 TYPE CORRECTION

def convert_to_int(value):
    if isinstance(value, str):
        return int(value.split('.')[0])
    elif isinstance(value, (int, float)):
        return int(value)
    else:
        return value

# ----------------------------------------------------------------------------------------------------------------------
# 7 DATEs and DATEf conversion (only PCLD)

# Conversion DATEs from yyyy to yyyy/mm/dd
def date_s_correction(input_date_s):
    try:
        corrected_date = datetime.strptime(input_date_s, '%Y').strftime('%Y/01/01')

        print("__________________________________________________________________________________________")
        print("                             START DATE  correction: DONE                                 ")
        print("__________________________________________________________________________________________")

        return corrected_date

    except ValueError:
        return input_date_s

# Conversion DATEf from yyyy to yyyy/mm/dd
def date_f_correction(input_date_f):
    try:
        corrected_date = datetime.strptime(input_date_f, '%Y').strftime('%Y/12/31')

        print("__________________________________________________________________________________________")
        print("                             END DATE  correction: DONE                                   ")
        print("__________________________________________________________________________________________")

        return corrected_date

    except ValueError:
        return input_date_f

# ----------------------------------------------------------------------------------------------------------------------
# 8 START DATE and END DATE conversion (only BGS)

def date_format(input_date):
    try:
        # Replace all '-' with '/'
        fixed_date = input_date.replace('-', '/')
        # Convert 'yyyy/mm/dd' strings into a datetime object
        date_object = datetime.strptime(fixed_date, '%Y/%m/%d')
        formatted_date = date_object.strftime('%Y/%m/%d')

        print("__________________________________________________________________________________________")
        print("                             START DATE and END DATE  correction: DONE                    ")
        print("__________________________________________________________________________________________")

        return formatted_date
    except ValueError:
        return 'error'

# ----------------------------------------------------------------------------------------------------------------------
# 9 START DATE and END DATE calculator (only NTMI)

def populate_start_date(row):
    if row['EVENT_DATE'] == "1697/06/07":
        return row['EVENT_DATE']
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "Other":
        return row['EVENT_DATE']
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == " Unknown ":
        return row['EVENT_DATE']
    elif pd.notna(row['EVENT_DATE']) and pd.notna(row['DATE_ACCUR']) and pd.notna(row['DATE_ACC_1']):
        return "1677/12/31"
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "1_Month":
        return pd.to_datetime(row['EVENT_DATE']).strftime("%Y/%m/01")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "2_Month") or (row['DATE_ACCUR'] == "2_Months")):
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(months=1)).strftime("%Y/%m/01")
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "1_Day":
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(days=1)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "1_Week":
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(weeks=1)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "1_Year":
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(years=1)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "10_Year") or (row['DATE_ACCUR'] == "10_Years")):
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(years=10)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "2_Year") or (row['DATE_ACCUR'] == "2_Years")):
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(years=2)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "20_Year") or (row['DATE_ACCUR'] == "20_Years")):
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(years=20)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "5_Year") or (row['DATE_ACCUR'] == "5_Years")):
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(years=5)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "6_Month") or (row['DATE_ACCUR'] == "6_Months")):
        return (pd.to_datetime(row['EVENT_DATE']) - pd.DateOffset(months=6)).strftime("%Y/%m/01")
    elif row['DATE_ACCUR'] == "Within the last 50 years":
        return "1970/01/01"
    elif row['DATE_ACC_1'] == "Within the last 50 years" and row['DATE_ACCUR'] == "other":
        return "1970/01/01"
    elif row['DATE_ACC_1'] == "2005-2011":
        return "2005/01/01"
    elif row['DATE_ACC_1'] == "2005-2008":
        return "2005/01/01"
    elif row['DATE_ACC_1'] == "1990-1991":
        return "1990/01/01"
    elif row['DATE_ACC_1'] == "1994-2000":
        return "1994/01/01"
    elif row['DATE_ACC_1'] == "2009-2010":
        return "2009/01/01"
    elif row['DATE_ACC_1'] == "3-5 Years approx " or row['DATE_ACC_1'] == "3-5 Years ":
        return "2011/01/01"
    elif row['DATE_ACC_1'] == "2 Days ":
        return "2015/09/10"
    elif pd.isna(row['DATE_ACC_1']) and pd.isna(row['DATE_ACCUR']) and pd.isna(row['EVENT_DATE']):
        return "1677/12/31"
    elif pd.isna(row['DATE_ACC_1']) and row['DATE_ACCUR'] == "Unknown":
        if not pd.isna(row['EVENT_DATE']):
            return pd.to_datetime(row['EVENT_DATE']).strftime("%Y/%m/%d")
        else:
            return "1677/12/31"
    elif pd.isna(row['DATE_ACC_1']) and pd.isna(row['DATE_ACCUR']) and not pd.isna(row['EVENT_DATE']):
        return pd.to_datetime(row['EVENT_DATE']).strftime("%Y/%m/%d")
    elif pd.isna(row['DATE_ACC_1']) and row['DATE_ACCUR']=="20_Years" and pd.isna(row['EVENT_DATE']):
        return "2000/01/01"

    print("__________________________________________________________________________________________")
    print("                             START DATE  correction: DONE                                 ")
    print("__________________________________________________________________________________________")

def populate_end_date(row):
    if pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "Other":
        return row['EVENT_DATE']
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == " Unknown ":
        return row['EVENT_DATE']
    elif pd.notna(row['EVENT_DATE']) and pd.notna(row['DATE_ACCUR']) and pd.notna(row['DATE_ACC_1']):
        return "2020/12/31"
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "1_Month":
        return pd.to_datetime(row['EVENT_DATE']).strftime("%Y/%m/%d")  # Fine del mese
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "2_Month") or (row['DATE_ACCUR'] == "2_Months")):
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(months=2)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "1_Day":
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(days=1)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "1_Week":
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(weeks=1)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and row['DATE_ACCUR'] == "1_Year":
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(years=1)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "10_Year") or (row['DATE_ACCUR'] == "10_Years")):
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(years=10)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "2_Year") or (row['DATE_ACCUR'] == "2_Years")):
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(years=2)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "20_Year") or (row['DATE_ACCUR'] == "20_Years")):
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(years=20)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "5_Year") or (row['DATE_ACCUR'] == "5_Years")):
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(years=5)).strftime("%Y/%m/%d")
    elif pd.notna(row['EVENT_DATE']) and ((row['DATE_ACCUR'] == "6_Month") or (row['DATE_ACCUR'] == "6_Months")):
        return (pd.to_datetime(row['EVENT_DATE']) + pd.DateOffset(months=6)).strftime("%Y/%m/%d")
    elif row['DATE_ACCUR'] == " Within the last 50 years ":
        return "2020/12/31"
    elif row['DATE_ACC_1'] == "Within the last 50 years" and row['DATE_ACCUR'] == "other":
        return "2020/12/31"
    elif row['DATE_ACC_1'] == "2005-2011":
        return "2011/12/31"
    elif row['DATE_ACC_1'] == "2005-2008":
        return "2008/12/31"
    elif row['DATE_ACC_1'] == "1990-1991":
        return "1991/12/31"
    elif row['DATE_ACC_1'] == "1994-2000":
        return "2000/12/31"
    elif row['DATE_ACC_1'] == "2009-2010":
        return "2010/12/31"
    elif row['DATE_ACC_1'] == "3-5 Years approx " or row['DATE_ACC_1'] == "3-5 Years ":
        return "2020/12/31"
    elif row['DATE_ACC_1'] == "2 Days ":
        return "2015/09/14"
    elif pd.isna(row['DATE_ACC_1']) and pd.isna(row['DATE_ACCUR']) and pd.isna(row['EVENT_DATE']):
        return "2020/12/31"
    elif pd.isna(row['DATE_ACC_1']) and row['DATE_ACCUR'] == "Unknown":
        if not pd.isna(row['EVENT_DATE']):
            return pd.to_datetime(row['EVENT_DATE']).strftime("%Y/%m/%d")
        else:
            return "2020/12/31"
    elif pd.isna(row['DATE_ACC_1']) and pd.isna(row['DATE_ACCUR']) and not pd.isna(row['EVENT_DATE']):
        return pd.to_datetime(row['EVENT_DATE']).strftime("%Y/%m/%d")
    elif pd.isna(row['DATE_ACC_1']) and row['DATE_ACCUR']=="20_Years" and pd.isna(row['EVENT_DATE']):
        return "2020/12/31"

    print("__________________________________________________________________________________________")
    print("                             END DATE  correction: DONE                                   ")
    print("__________________________________________________________________________________________")

# ----------------------------------------------------------------------------------------------------------------------
# 10 - START DATE and END DATE calculator (only SLIDO)

def start_date_SLIDO(row):
    if not pd.isnull(row["MONTH"]) and row["MONTH"] == "0" or not pd.isnull(row["DAY"]) and row["DAY"] == "0" or not pd.isnull(row["YEAR"]) and row["YEAR"] == "0.0":
        return "1677/12/31"

    elif pd.isnull(row["YEAR"]) and pd.isnull(row["MONTH"]) and pd.isnull(row["DAY"]) and pd.isnull(
            row["REACTIVATI"]) and pd.isnull(row["DATE_RANGE"]):
        return "1677/12/31"

    elif not pd.isnull(row["YEAR"]):
        year = int(row["YEAR"])
        month = int(row["MONTH"]) if not pd.isnull(row["MONTH"]) else 1
        day = int(row["DAY"]) if not pd.isnull(row["DAY"]) else 1
        return f"{year:04d}/{month:02d}/{day:02d}"

    elif not pd.isnull(row["REACTIVATI"]):
        reactivati_date_parts = row["REACTIVATI"].split('/')  # Dividi la data di REACTIVATI
        year = int(reactivati_date_parts[0])  # Estrai l'anno
        month = int(reactivati_date_parts[1]) if len(reactivati_date_parts) > 1 else (int(row["MONTH"]) if not pd.isnull(row["MONTH"]) else 1)
        day = int(reactivati_date_parts[2]) if len(reactivati_date_parts) > 2 else (int(row["DAY"]) if not pd.isnull(row["DAY"]) else 1)
        return f"{year:04d}/{month:02d}/{day:02d}"

    elif not pd.isnull(row["DATE_RANGE"]):
        date_range_parts = row["DATE_RANGE"].split('/')  # Dividi la data di DATE_RANGE
        year = int(date_range_parts[0])  # Estrai l'anno
        month = int(date_range_parts[1]) if len(date_range_parts) > 1 else (int(row["MONTH"]) if not pd.isnull(row["MONTH"]) else 1)
        day = int(date_range_parts[2]) if len(date_range_parts) > 2 else (int(row["DAY"]) if not pd.isnull(row["DAY"]) else 1)
        return f"{year:04d}/{month:02d}/{day:02d}"

    else:
        print("__________________________________________________________________________________________")
        print("                             START DATE  correction: DONE                                 ")
        print("__________________________________________________________________________________________")

        return "1677/12/31"

def end_date_SLIDO(row):
    def last_day_of_month(year, month):
        return calendar.monthrange(year, month)[1]

    def last_month_of_year(year):
        return 12

    if not pd.isnull(row["MONTHe"]) and row["MONTHe"] == "0" or not pd.isnull(row["DAYe"]) and row["DAYe"] == "0" or not pd.isnull(row["YEARe"]) and row["YEARe"] == "0.0":
        return "2020/12/31"

    elif pd.isnull(row["YEARe"]) and pd.isnull(row["MONTHe"]) and pd.isnull(row["DAYe"]) and pd.isnull(
            row["REACTIVATIe"]) and pd.isnull(row["DATE_RANGEe"]):
        return "2020/12/31"

    elif not pd.isnull(row["YEARe"]):
        year = int(row["YEARe"])
        month = int(row["MONTHe"]) if not pd.isnull(row["MONTHe"]) else last_month_of_year(year)
        day = int(row["DAYe"]) if not pd.isnull(row["DAYe"]) else last_day_of_month(year, month)
        return f"{year:04d}/{month:02d}/{day:02d}"

    elif not pd.isnull(row["REACTIVATIe"]):
        reactivati_date_parts = row["REACTIVATIe"].split('/')  # Dividi la data di REACTIVATI
        year = int(reactivati_date_parts[0])  # Estrai l'anno
        month = int(reactivati_date_parts[1]) if len(reactivati_date_parts) > 1 else (
            int(row["MONTHe"]) if not pd.isnull(row["MONTHe"]) else last_month_of_year(year))
        day = int(reactivati_date_parts[2]) if len(reactivati_date_parts) > 2 else (
            int(row["DAYe"]) if not pd.isnull(row["DAYe"]) else last_day_of_month(year, month))
        return f"{year:04d}/{month:02d}/{day:02d}"

    elif not pd.isnull(row["DATE_RANGEe"]):
        date_range_parts = row["DATE_RANGEe"].split('/')  # Dividi la data di DATE_RANGE
        year = int(date_range_parts[0])  # Estrai l'anno
        month = int(date_range_parts[1]) if len(date_range_parts) > 1 else (
            int(row["MONTHe"]) if not pd.isnull(row["MONTHe"]) else last_month_of_year(year))
        day = int(date_range_parts[2]) if len(date_range_parts) > 2 else (
            int(row["DAYe"]) if not pd.isnull(row["DAYe"]) else last_day_of_month(year, month))
        return f"{year:04d}/{month:02d}/{day:02d}"

    else:
        print("__________________________________________________________________________________________")
        print("                             END DATE  correction: DONE                                   ")
        print("__________________________________________________________________________________________")

        return "2020/12/31"

# ----------------------------------------------------------------------------------------------------------------------
# 11 - START DATE and END DATE calculator (only CAFLAG)
# START DATE date composer

def compose_start_date(year, month, day):
    # Replace "ND" YEAR values with the oldest date present into the dataset
    if year == "ND":
        return datetime(1828, 2, 2).strftime('%Y/%m/%d')  # Restituisce la data 1828/02/02 nel formato desiderato
    # Replace "pre-" or "pre" YEAR values with the oldest date present into the dataset
    elif isinstance(year, str) and year.startswith("pre-"):
        return datetime(1828, 2, 2).strftime('%Y/%m/%d')
    elif isinstance(year, str) and year.startswith("pre"):
        return datetime(1828, 2, 2).strftime('%Y/%m/%d')
    else:
        year_value = int(year) if year != "ND" \
            else 1828
        month_value = 2 if year == 1828 \
            else int(month) if month != "ND" and year != 1828 \
            else 1
        day_value = 2 if year == 1828 \
            else int(day) if day != "ND" and year != 1828 \
            else 1 if day == "ND" and year != 1828 \
            else 1
        return datetime(year_value, month_value, day_value).strftime('%Y/%m/%d')

def compose_end_date(year, month, day):
    # Replace "ND" YEAR values with the latest date present into the dataset
    if year == "ND":
        return datetime(2017, 3, 15).strftime('%Y/%m/%d')
    # Replace "pre-" or "pre" YEAR values with the latest date present into the dataset
    elif isinstance(year, str) and year.startswith("pre-"):
        return datetime(2017, 3, 15).strftime('%Y/%m/%d')
    elif isinstance(year, str) and year.startswith("pre"):
        return datetime(2017, 3, 15).strftime('%Y/%m/%d')
    else:
        year_value = int(year) if year != "ND" \
            else 2017
        month_value = 3 if year == 2017 \
            else int(month) if month != "ND" and year != 2017 \
            else 1
        day_value = 15 if year == 2017 \
            else int(day) if day != "ND" and year != 2017 \
            else 1 if day == "ND" and year != 2017 \
            else 1
        return datetime(year_value, month_value, day_value).strftime('%Y/%m/%d')

# -----------------------------------------------------------------------------------------------------------------------