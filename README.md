- - -
# <p align="center"> UNIFIED GLOBAL LANDSLIDE CATALOGUE</p>

## <p align="center"> Polygonal catalogue </p>

----------------------------------------------------------------------------------------------------------------

## :red_circle: Authors

----------------------------------------------------------------------------------------------------------------
- [@Saverio Mancino](https://github.com/RavyHollow) - PhD Student (Dept. Geo-enviromental science - University of Bari).
- [@Anna Sblano](https://github.com/Anita2333) - Research Fellow (Dept. Geo-enviromental science - University of Bari).
- [@Francesco Paolo Lovergine](https://github.com/fpl) - Researcher (Institute for the Electromagnetic Survey of the Atmosphere - National Research Council of Italy).
- Tushar Sethi - Director (Margosa Environmental Solutions Ltd)
- [@Giuseppe Amatulli](https://github.com/selvaje) - PhD Researcher (School of the Environment - Yale University).
- Domenico Capolongo - PhD Professor (Dept. Geo-enviromental science - University of Bari).

----------------------------------------------------------------------------------------------------------------

## :red_circle: Project description

The main purpose of this project is to generate a single global-scale landslide dataset that collects and standardizes within it all open source global, national, 
and sub-national landslide datasets, provided with spatial and temporal accuracy details, along with several general information about each single record. 
Researchers that are willing to contribute with additional landslide points and polygons can keep in touch with [@Saverio Mancino](https://github.com/RavyHollow). 
The Unified Global Landslide Catalogue (UGLC) scientifcial and technical publication is under preparation and a will be submmited to ESSD Copernicus in early 2025.

----------------------------------------------------------------------------------------------------------------

## :red_circle: License
The whole code is published under the [MIT License](files/LICENSE.txt).

----------------------------------------------------------------------------------------------------------------

## :red_circle: Data availability
The catalogues data are available in these googledrive repositories, as full catalogue in .csv format (with '|' as separator) and as a tile in .gpkg format ([see tiling scheme](https://github.com/UnibaGEO/UGLC/blob/master/README.md#red_circle-tiling-system)).
They're distributed under the licence [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) 


| CATALOGUE TYPE                 | NUMBER OF RECORDS | FILES REPOSITORY                                                                                                              |
|--------------------------------|-------------------|-------------------------------------------------------------------------------------------------------------------------------|
| UGLC Point Catalogue files     | 1061450 points    | :leftwards_arrow_with_hook: [POINT CATALOGUE](https://github.com/UnibaGEO/UGLC_point)                                         |
| UGLC Polygonal Catalogue files | 984126 polygons   | FULL CATALOGUE [download :arrow_down:](https://drive.google.com/file/d/1HbQL4qt0UmgC5jSmPIhIeOCkAojnVzYa/view?usp=sharing)    |
|                                |                   | TILED CATALOGUE [download :arrow_down:](https://drive.google.com/drive/folders/1OGHdiTZA3E9pfDV20WQ_OT1OpbBxf3WT?usp=sharing) |


![Licenza Dati: CC BY 4.0](https://licensebuttons.net/l/by/4.0/88x31.png)

----------------------------------------------------------------------------------------------------------------

## :red_circle: Attribute fields summary

| ATTRIBUTE        | TYPE            |
|------------------|-----------------|
| WKT_GEOM         | Well known text |
| NEW DATASET      | String          |
| ID               | Int             |
| OLD DATASET      | String          |
| OLD ID           | String          |
| VERSION          | String          |
| COUNTRY          | String          |
| ACCURACY         | Int             |
| START DATE       | Date            |
| END DATE         | Date            |
| TYPE             | String          |
| PHYSICAL FACTORS | String          |
| RELIABILITY      | Int             |
| RECORD TYPE      | String          |
| FATALITIES       | Int             |
| INJURIES         | Int             |
| NOTES            | String          |
| LINK             | String          |

----------------------------------------------------------------------------------------------------------------

## :red_circle: Attributes description


- <b> WKT_GEOM: </b> The contents of this field contain information about the georeferencing of each polygon described in the dataframe using the WGS84 reference system.


- <b> NEW DATASET: </b> the content of this field represents the name of the new dataframe's identifying abbreviation: "UGLC".


- <b> ID: </b> the content of this field contains a unique ID for each landslide event included into the UGLC dataset.


- <b> OLD DATASET: </b> the contents of this field represent the name of the native dataset used into the UGLC creation:

    | POLYGONAL DATASET |
    |-------------------|

    | REFERING                                                                                                                                                                                 | NAME                                                                               | N° POLYGONS | LICENSE                                                                               | DOWNLOAD  | IMPLEMENTED           |
    |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-------------|---------------------------------------------------------------------------------------|-----------|-----------------------|
    | [01_PALI](https://zenodo.org/records/7057656)                                                                                                                                            | Patagonian Andes Landslide Inventory (Morales et al., 2022)                        | 10026       | [LICENSE](https://creativecommons.org/licenses/by/4.0/legalcode)                      | free      | :heavy_check_mark:    |
    | [02_MAL](https://zenodo.org/records/6107187)                                                                                                                                             | Sabah (Malaysia)Landslides triggered by the 2015 6.0 Mw earthquake                 | 5198        | [LICENSE](https://creativecommons.org/licenses/by/4.0/legalcode)                      | free      | :heavy_check_mark:    |
    | [03_PH](https://zenodo.org/records/7520726)                                                                                                                                              | Cotabato - Davao del Sur (Philippines) Landslides triggered by the 2019 earthquake | 10593       | [LICENSE](https://creativecommons.org/licenses/by/4.0/legalcode)                      | free      | :heavy_check_mark:    |
    | [04_HLD](https://zenodo.org/records/8308313)                                                                                                                                             | Haiti landslide dataset                                                            | 4178        | [LICENSE](https://creativecommons.org/licenses/by/4.0/legalcode)                      | on demand | :heavy_check_mark:    |
    | [05_ASM](https://www.data.gov.uk/dataset/d614bc9b-2696-4bd6-be01-b461cee575d1/polygon-inventory-of-12-920-asia-summer-monsoon-asm-triggered-landslides-in-nepal-nerc-grant-ne-l002582-1) | ASIA summer moonsoon landslide dataset                                             | 12920       | [LICENSE](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) | free      | :heavy_check_mark:    |
    | [06_GEUS_DN](https://figshare.com/articles/dataset/Danish_landslide_inventory_211104/16965439/2)                                                                                         | GEUS national landslide inventory for Denmark                                      | 3202        | [LICENSE](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) | free      | :heavy_check_mark:    |
    | [07_UTH](https://gis.utah.gov/data/geoscience/landslides/)                                                                                                                               | Utah landslide Inventory polygons                                                  | 2381        | [LICENSE](https://gis.utah.gov/about/policy/license-disclaimer/)                      | free      | :heavy_check_mark:    |
    | [08_JLD](https://zenodo.org/records/3775870)                                                                                                                                             | Japan landslide dataset for semantic segmentation                                  | 331         | [LICENSE](https://creativecommons.org/licenses/by/4.0/legalcode)                      | free      | :heavy_check_mark:    |
    | [09_COOLR](https://maps.nccs.nasa.gov/arcgis/apps/MapAndAppGallery/index.html?appid=574f26408683485799d02e857e5d9521)                                                                    | Cooperative Open Online Landslide Repository - Report and Event Polygons (NASA)    | 20056       | [LICENSE](https://maps.nccs.nasa.gov/arcgis/apps/MapAndAppGallery/index.html?appid=574f26408683485799d02e857e5d9521)                      | free      | :heavy_check_mark:    |
    | [10_ETGFI](https://www.sciencebase.gov/catalog/item/583f4114e4b04fc80e3c4a1a)                                                                                                            | ETGFI - Earthquake Triggered Ground Failure Inventories (USGS)                     | 491840      | [LICENSE](https://www.sciencebase.gov/catalog/item/583f4114e4b04fc80e3c4a1a)                      | free      | :heavy_check_mark:    |
    | [11_IFFI](https://idrogeo-isprambiente-it.translate.goog/app/page/open-data?_x_tr_sl=en&_x_tr_tl=it&_x_tr_hl=it&_x_tr_pto=sc&_x_tr_hist=true)                                           | IFFI - Inventario fenomeni franosi in Italia                                       | 423401      | [LICENSE](https://creativecommons.org/licenses/by/4.0/legalcode)                      | free      | :heavy_check_mark:    |


- <b> OLD ID: </b> the contents of this field represent the identifying id assigned to this row in the source dataset (if any)


- <b> VERSION: </b> the contents of this field represent the latest updated version of the original dataset used (if specified)


- <b> COUNTRY: </b> the content of this field represents the country where the record was located (where missing it was derived using its coordinates)


- <b> ACCURACY: </b> the content of this field represents the precision in meters of the relative deviation of the geo-referenced polygon from 
    the actual landslide (if there is one), where it is not clearly specified is inferred based on the information present in the record. 
    While the total absence of accuracy information becomes a NaN value for identify spatially uncertain records, represented by the value '-99999'.


- <b> START DATE: </b> the contents of this field represent the date of the record (if specified exactly in the source dataset) 
    and in that case it will coincide with the END DATE field (format:ISO 8601:YYYY/MM/DD).
    In case the record date is not present or clearly explicit, this field will contain the start date of the dataset acquisition time range;
    so the date inside this field will not be coincident with the END DATE field, implying the temporal uncertainty of that record.
    In case of records where start date could not be derived at all, or if the record start date is before '1677/12/31', this field will be 
    set as '1678/01/01' due to pandas time limit.


- <b> END DATE: </b> the contents of this field represent the date of the record (if specified exactly in the source dataset) 
    and in that case it will coincide with the START DATE field (format:ISO 8601:YYYY/MM/DD).
    In case the record date is not present or clearly explicit, this field will contain the end date of the dataset acquisition time range;
    so the date inside this field will not be coincident with the START DATE field, implying the temporal uncertainty of that record.


- <b> TYPE: </b> Contains information about the geological and kinematic type of the landslide record, standardized using
    the extended classification of Varnes including also other common gravitational surface instability phenomena (Hungr et al., 2014).
    These type categories are standardized using this reference table: 
  
    | LANDSLIDE CATEGORY           |
    |------------------------------|
    | <i>(description)</i>         |
    | complex                      |
    | soil creep                   | 
    | debris flow                  |  
    | earth flow                   |
    | lahar                        |
    | earth slide                  |
    | mudslide                     |
    | riverbank collapse           |
    | rock slide                   |
    | rock fall                    |
    | rotational sliding           |
    | translational sliding        |
    | earth spreading              |
    | rock spreading               |
    | mud flow                     |
    | sinkhole                     |
    | ND                           |


- <b>PHYSICAL FACTORS:</b> This field encompasses the physical factors contributing actively to the landslide activation, categorized 
    into predisposing (PR), preparatory (P) and triggering (T) factors. Predisposing factors include invariant characteristics 
    such as geology, topography, and land use; preparatory factors refer to monitorable cyclical changes like seasonal variations 
    in saturation, weathering, or fire-induced alterations while triggering factors involve impulsive events such as 
    earthquakes, intense rainfall, or volcanic activity. 
    The category of Predisposing factors (PR) was not considered in our classification because it was absent in the native 
    data. Therefore, only the categories of Preparatory (P) and Triggering (T) factors were considered in the classification 
    of physical factors of landslides in this catalog.
    These categories are standardized using this reference table:
  
    | PHYSICAL FACTORS                        | IDENTIFYING ABBREVIATION |
    |-----------------------------------------|--------------------------|
    | <i>(description)</i>                    | <i>(value)</i>           | 
    | Rainfall activity                       | rainfall (T)             | 
    | Seismic activity                        | seismic (T)              | 
    | Volcanic activity                       | volcanic (T)             |  
    | Human-induced factors                   | anthropic (T,P)          | 
    | Climatic factors                        | climate (T,P)            | 
    | Post-fire conditions                    | postfire (P)             |
    | Post-deforestation processes conditions | deforestation (P)        |
    | Erosional and biological factors        | natural (T,P)            | 
    | Not defined                             | ND                       | 


- <b> RELIABILITY: </b> the content of this field represents the reliability of the data based on a decision table that takes into 
    account spatial accuracy (ACCURACY) and temporal accuracy (START DATE, END DATE):

    | SPATIAL RELIABILITY    | TEMPORAL RELIABILITY           | RELIABILITY DESCRIPTION          | CLASS          |
    |------------------------|--------------------------------|----------------------------------|----------------|
    | <i>(meters)</i>        | <i>(START DATE = END DATE)</i> | <i>(Description)</i>             | <i>(value)</i> |
    | ( <100 m )             | TRUE                           | Exact point                      | 1              | 
    | ( <100 m )             | FALSE                          | Almost exact point               | 2              |
    | ( >100 m and <250 m )  | TRUE                           | Very high reliability point      | 3              | 
    | ( >100 m and <250 m )  | FALSE                          | High reliability point           | 4              |  
    | ( >250 m and <500 m )  | TRUE                           | Medium reliability point         | 5              |
    | ( >250 m and <500 m )  | FALSE                          | Low reliability point            | 6              | 
    | ( >500 m and <1000 m ) | TRUE                           | Very low reliability point       | 7              | 
    | ( >500 m and <1000 m ) | FALSE                          | Poor reliability point           | 8              |
    | ( >1000 m )            | TRUE and FALSE                 | Point with uncertain reliability | 9              | 
    | ( -99999)              | TRUE and FALSE                 | Unreliable point                 | 10             | 


- <b> RECORD TYPE: </b>  The contents of this field contain information regarding the record type: <u>report</u>, 
    <u>event</u>.
    
    - Report catalogs are usually landslide reports that typically collect a lot of detailed technical information 
    about individual landslide events.
  
    - Event catalogs, on the other hand, generally focus on summarizing landslide events 
    triggered by episodic events (such as heavy rains, earthquakes, eruptions, etc.) with less technical information and 
    more statistical details, without delving into the specifics of each event.


- <b> FATALITIES: </b> the content of this field contains the number of fatalities related to the record (if explicit), where the NaN values are represented by the value -99999
  

- <b> INJURIES: </b> the content of this field contains the number of injuries related to the record (if explicit), where the NaN values are represented by the value -99999


- <b> NOTES: </b> the content of this field contains the notes and information relate to the record (if explicit)


- <b> LINKS: </b>  the content of this field contains the link to the source of the record report or study (if explicit)

--------------------------------------------------------

## :red_circle: Folder Structure

--------------------------------------------------------
<img alt="Dataframe Folder Structure" src="files/dataframe_structure.png"/>
<p align="center"><i> Folder Structure Scheme </i></p>

--------------------------------------------------------


The entire UGLC structure is allocated in 2 main repositories:

- GitHub Scripts Repository (GSR)
- Drive Files Repository (DFR)

The GSR contains 5 main folders :
- /input
 
    This folder contains the "native_datasets" subfolder, which contains the standardizer scripts ("N_DATAFRAME_standardizer.py")
    which read the downloaded files into the DFR 'input/download' subfolder (containing native datasets as .csv/.shp/.gpkg etc.
    downloaded from the source sites (Entities, Government agencies, Universities, Various repositories etc.)
    and create a standardized .csv ready to be converted into the UGLC format, and save it (as "N_DATAFRAME_native.csv")
    into the DFR 'input/native_dataset' subfolder.

- /csv

     This folder contains one subfolder named after each different native datasets ("N_DATAFRAME") contains the converting scripts
    ("N_DATAFRAME_converter.py") and the lookup tables ("NN_DATAFRAME_lookuptables.json") which read the native datasets from
    the DFR 'input/native_dataset' subfolder, then filter and convert each one into the UGLC standard format, using also the functions from the 'lib' folder,
    and save them (as "N_DATAFRAME_converted.csv") into the DFR 'output/converted_csv' subfolder.

- /output

    This folder contains the unifier script ("unifier.py") that read all the converted datasets from the DFR 'output/converted_csv'
    subfolder, then merge and filter them for generating the final UGLC dataframe ("UGLC_poly_full.csv") and the tiled verion ("UGLC_poly_tile_i_j.gpkg"),
    saving everything into the DFR 'output' folder.
  
- /lib

    This folder contains the functions script ("function_collection.py") which are called from the converter scripts into the
    GPR for various data conversion.

- /files
  
    This folder contains all the files used by this readme file, like pictures and the license file.

--------------------------------------------------------

## :red_circle: Tiling system

<img alt="Dataframe Folder Structure" src="files/UGLC_tile_grid_map.jpeg"/>

The UGLC catalog is also available in GeoPackage format, divided into 105 tiles that cover the entire Earth's surface.
Each tile includes a Tile_ID attribute (_i_j) for unique identification within the grid: 

    i (longitude step) = [0-15]
    j (latitude step) = [0-7]

Empty tiles are automatically excluded from storage, ensuring optimized file management and performance.

--------------------------------------------------------
## :red_circle: Catalogue Data Analysis

In order to better understand the information content of both catalogues (point and polygonal), several statistical analysis
were conducted to explore key aspects of the contained data. This information is essential to ensure appropriate and targeted
use of the catalogues, highlighting their potential for future scientific developments.\
The analysis demonstrates a pronounced disparity in the geographical distribution of landslide records across continents. 
Within the point catalogue, Europe exhibits the highest representation (61.55%) followed by North America (19.63%) and Asia 
(10.17%). Africa, South America and Oceania collectively constitute a really low share (below 3.97%).\
While, the polygonal catalogue presents a different distribution pattern, with Asia leading with Europe (45.09% and 43.40%),
followed by North America (8.73\%). Also in this case, Africa, South America and Oceania collectively constitute a negligible
portion (1.43%).

<img alt="UGLC Data Distribution per Continent for both Point and Polygonal Catalogue" src="files/UGLC Data Distribution per Continent for both Point and Polygonal Catalogue.png"/>

This imbalance becomes more apparent by going into more detail with a state-by-state analysis, showing how native 
datasets represent landslide records with an unbalanced distribution in both density and geographic distribution.\
Particularly from the state-wise density data, it can be seen that some relatively small states like Italy, UK, 
New Zealand, etc. lead the landslide data collection along with large countries such as the USA and China 
(sometimes heavily surpassing them, as in the case of Italy, which alone contributes more than 57% of the whole catalogue).\
This shows a different attention to landslide phenomena in more affected countries, also highlighting a different 
socioeconomic influence devoted to the study and analysis of landslides in different countries. Although, in contrast to
the high density of studies available for these regions, much of the data (particularly from European and Asian areas) 
are not openly accessible.\
Consequently, the analysis was affected by restrictions applied to certain datasets that are not publicly available.

<img alt="UGLC Landslide Point Density Per State" src="files/UGLC Landslide Point Density Per State.png"/>

Temporal consistency analysis highlighted the heterogeneous data time consistency across datasets, that required a 
significant effort to standardize and interpret temporal data while addressing discrepancies in formatting and granularity.\
Native datasets varied widely in their time precision, ranging from exact event dates to broader temporal ranges 
(e.g., decades or centuries). For records with incomplete or poorly formatted temporal data, standardization efforts 
involved assigning representative time ranges based on the available context, ensuring logical alignment with the 
recorded phenomena. This approach not only improved temporal consistency but also enhanced the utility of the catalogue
by preserving valuable, albeit imprecise, historical data. This aims to mitigate the risk of data misinterpretation
resulting from inconsistent native data formats, providing a temporal reliable catalogue.

<img alt="UGLC point data Temporal Consistency per Native Dataset" src="files/UGLC point data Temporal Consistency per Native Dataset.png"/>

Along with temporal accuracy, spatial accuracy is a critical factor in cataloguing these phenomena, as it determines the 
geospatial reliability of each record.\
Native data sets often presented difficulties, including poorly formatted coordinates, varying levels of precision, 
and inconsistencies in georeferencing methods. To address these issues, a standardized spatial accuracy parameter was 
established, allowing for a consistent representation on a meter scale of the spatial reliability of each record.\
Accuracy was converted when native data provided were on other scales, while for records with incomplete or ambiguous 
location data, an expert interpretation was employed to estimate the probable accuracy. This process involved 
cross-referencing auxiliary information, such as nearby landmarks or descriptive metadata, to determine coordinates 
that closely approximated the event's actual location.\
This methodology ensured that even imprecise data could be meaningfully integrated, significantly reducing the
proportion of records categorized as no-data in spatial accuracy.
The resulting accuracy distribution ranges from highly precise values (<10 meters) to broader approximations
(>10 kilometers), reflecting the inherent variability in quality and reporting practices of the source

<img alt="UGLC Point Data Accuracy Distribution" src="files/UGLC_Point_Data_Accuracy_Distribution.png"/>

Therefore, the reliability attribute introduced in this catalogue, calculated on the basis of spatial and temporal 
accuracy, reflects the general robustness of each individual record after the standardization processes.\
Showing for both catalogues (point and polygonal), an extremely high record reliability (class 1 and 2), whereas 
only in the point catalogue, the data with a lower reliability class together do not exceed 15\% of the catalogue.\
However, all the spatial and temporal standardization process establishes a reliable framework, summarized by the 
reliability class parameter.\
Making the catalogue suitable for future precise applications such as spatial modelling, 
risk assessment, and policy development.

<img alt="UGLC Reliablity Distribution for both Point and Polygon Catalogue" src="files/UGLC Reliablity Distribution for both Point and Polygon Catalogue.png"/>

From further data analysis, it was also possible to highlight the distribution of the different standardized landslide 
types found within the unified catalogue with detail also on the variance of each type based on the information in the 
native record.\
A major difficulty in the creation of this huge standardized catalogue was the condensation of heterogeneous data to 
achieve information consistency. Especially in a context such as geology, where extreme variance in the nomenclature 
of different types is often a stumbling block in data intercommunication.\
In fact, the observed variance reflects the extent to which native data sources contributed to the different 
interpretation of each standardized landslide type.\
This diversity comes from the consolidation of extremely heterogeneous datasets, in which different terminologies, 
classification schemes, and levels of granularity were harmonized into standardized categories, while also recovering 
data on the large amount of typos and data entry errors. Types with greater variance, such as “complex” or “earth flow,” 
therefore indicate the presence of a higher rate of interpreted data than data on the natively more unambiguous and 
consistent and therefore easily interpreted typology such as for “rockfall” or “sinkhole” types.

<img alt="UGLC Standardized Type Distribution Magnitude vs Variance" src="files/UGLC Standardized Type Distribution Magnitude vs Variance.png"/>

It was also possible to analyse the distribution of various physical factors associated to each landslide catalogued record.\
The graph reveals a higher prevalence of missing informations about physical factors, followed by Triggering factors (T) 
and Preparatory factors (P), without representation of Predisposing factors (PR).\
The dominance of common Triggering factors like rainfall and seismic activity, highlights the statistical prevalence of 
these phenomena in native catalogues. However, this distribution is also clearly influenced by the uneven geographical 
coverage of the data, where landslides tend to occur more frequently in regions where these triggering factors are more 
prominent, underscoring the need to address spatial heterogeneity in future data collection to enhance global 
representativeness.

<img alt="UGLC point data Physical Factors Distribution" src="files/UGLC point data Physical Factors Distribution.png"/>

Analyzing the overall distribution of the various standardized landslide types in the catalogue shows how the frequencies
of each type of landslide vary widely.\
The graph reveals how the undefined categories ('ND') are the majority, showing native datasets lack of information on 
the kinematics for each landslide record.\
However, for non-null categories, the types 'complex', 'earth slide', 'rock fall' and 'soil creep' are the most prevalent, 
while types such as 'lahar' and 'earth spreading' are minimally represented.\
The spatial heterogeneity of the dataset is evident, with dense clusters in regions widely studied as more climatically 
and geologically active, such as South Asia and Central America, and under-representation in areas such as Africa and 
Russia due to data gaps related to likely difficulty in mapping or restrictions in data availability.\
The impact of data availability and uneven data resolution on the global representation of landslides is highlighted 
even more.

<img alt="UGLC Landslide Points Type distribution" src="files/UGLC Landslide Points Type distribution.png"/>

--------------------------------------------------------
