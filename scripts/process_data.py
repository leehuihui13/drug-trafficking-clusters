import pandas as pd
import logging
import googlemaps
import pycountry_convert as pc
from sklearn.preprocessing import OneHotEncoder



def import_data():
    """
    Importing data from Excel files.
    """
    # Importing drug data
    data_sheets = pd.read_excel('data/IDS-data-2011_2022-Nov23.xlsx', sheet_name=None, header=0)
    data = pd.concat(data_sheets.values())
    data = data.reset_index(drop=True)

    # Importing drug list
    drug_data = pd.read_excel('data/drug_list.xlsx', header=0)
    drug_classes = drug_data.groupby('Drug class/ group').agg({'Drug Name/Type': lambda x: list(x)}).reset_index()

    return data, drug_classes

def explore_data(data):
    """
    Exploring the imported data and returns basic information.

    Args:
        data (DataFrame): The DataFrame containing the imported data.

    Returns:
        Dictionary with the following information:
            - 'columns': List of column names
            - 'data_types': Data types of columns
            - 'summary_statistics': Summary statistics of numerical columns
            - 'missing_values': Number of missing values in each column
    """
    # Displaying basic information about the data
    columns = data.columns.tolist()
    data_types = data.dtypes.to_dict()

    # Data types and summary statistics
    summary_statistics = data.describe().to_dict()

    # Checking for missing values
    missing_values = data.isna().sum().to_dict()

    return {
        'columns': columns,
        'data_types': data_types,
        'summary_statistics': summary_statistics,
        'missing_values': missing_values
    }

def preprocess_data(data, drug_classes, gmap_key):
    """
    Preprocess the data before analysis.

    Args:
        data (DataFrame): The DataFrame containing the imported data.

    Returns:
        DataFrame: The preprocessed DataFrame
    """

    # Part 1: Converting Date column to datetime object
    data = convert_to_datetime(data)

    # Part 2: Adding geospatial data
    data = add_geospatial_data(data, gmap_key)

    # Part 3: Cleaning
    data = add_drug_classes(data, drug_classes)

    # Part 4: Cleaning and encoding categorical variables
    data = clean_and_encode_categorical(data)

    return data

def convert_to_datetime(data):
    """
    Convert the 'DateDDMMYYYY' column to datetime object.

    Args:
        data (DataFrame): The DataFrame containing the imported data.

    Returns:
        DataFrame: The DataFrame with the 'DateDDMMYYYY' column converted to datetime object.
    """
    data['DateDDMMYYYY'] = pd.to_datetime(data['DateDDMMYYYY'], format='mixed')
    return data


def add_geospatial_data(data, gmaps_key):
    """
    Add geospatial data using 'Countryofseizure' column.

    Args:
        data (DataFrame): The DataFrame containing the imported data.

    Returns:
        DataFrame: The DataFrame with added geospatial data attributes.
    """
    gmaps = googlemaps.Client(key=gmaps_key)

    countries = data['Countryofseizure'].value_counts().index
    lat_data = dict()
    lng_data = dict()
    
    for country in countries:
        try:
            geocode_result = gmaps.geocode(country)
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            lat_data[country], lng_data[country] = lat, lng

        except IndexError as e:
            logging.exception(e)

    data['lat'] = data['Countryofseizure'].map(lat_data)
    data['lng'] = data['Countryofseizure'].map(lng_data)

    return data


def add_drug_classes(data, drug_classes):
    """
    Add drug classes data using 'Drug' column.

    Args:
        data (DataFrame): The DataFrame containing the imported data.

    Returns:
        DataFrame: The DataFrame with added 'Drug class/ group' attribute.
    """
    drug_names = pd.unique(data['Drug'])

    # Initialize a dictionary to store drug-class mappings
    drug_class_mapping = dict()

    # Match drug names with drug classes
    for drug_name in drug_names:
        matched_class = 'Unspecified'
        for index, row in drug_classes.iterrows():
            if drug_name.lower().strip() in [d.lower().strip() for d in row['Drug Name/Type']]:
                matched_class = row['Drug class/ group']
                break
        drug_class_mapping[drug_name] = matched_class

    data['Drug class/ group'] = data['Drug'].map(drug_class_mapping)

    return data

def clean_and_encode_categorical(data):
    """
    Clean and encode categorical variables 'Drug class/ group', 'Meanoftransportation' and 'Sitetypeoflocationofseizure'.

    Args:
        data (DataFrame): The DataFrame containing the imported data.
        
    Returns:
        DataFrame: The DataFrame with encoded categorical variables.
    """
    data['Drug class/ group'] = data['Drug class/ group'].astype(str).str.capitalize().astype('category')
    data['Meansoftransportation'] = data['Meansoftransportation'].astype(str).str.capitalize().astype('category')
    data['Sitetypeoflocationofseizure'] = data['Sitetypeoflocationofseizure'].astype(str).str.capitalize().astype('category')

    cat_columns = ["Drug class/ group", "Meansoftransportation", "Sitetypeoflocationofseizure"]
    onehotencoder = OneHotEncoder(sparse_output=False)
    X = onehotencoder.fit_transform(data[cat_columns])
    one_hot_df = pd.DataFrame(X, columns=onehotencoder.get_feature_names_out(cat_columns))
    data = pd.concat([data, one_hot_df], axis=1)

    return data

def export_data(data):
    """
    Exporting processed data as a CSV file.
    """
    data.to_csv('data/processed_data.csv', index=False)
    print("Processed data has been exported.")


# Importing data
data, drug_classes = import_data()

# Exploring data
explore_data(data)

# Preprocessing data
api_key = input("Input API key")
processed_data = preprocess_data(data, drug_classes, gmap_key=api_key)

# Exporting processed data
export_data(processed_data)

