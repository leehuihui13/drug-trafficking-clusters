import pandas as pd
from sklearn.preprocessing import StandardScaler
from kmodes.kprototypes import KPrototypes
from sklearn.metrics import silhouette_score



def import_data():
    """
    Importing processed data from csv file.
    """
    data = pd.read_csv('data/processed_data.csv', header=0, low_memory=False)
    data['DateDDMMYYYY'] = pd.to_datetime(data['DateDDMMYYYY'], format='mixed')

    return data

def filter_data(data):
    """
    Filtering attributes from data used for clustering model.

    Args:
        data (DataFrame): The DataFrame containing the processed data.

    Returns:
        filtered_data (DataFrame): The DataFrame containing the filtered data.
    """

    # Filtering off data with unspecified drug class
    data = data.loc[data['Drug class/ group_Unspecified'] != 1, :]

    # Filtering for variables of interest
    all_variables = data.columns
    prefixes = ['DateDDMMYYYY', 'lat', 'lng', 'Drug class/ group_', 'Meansoftransportation_', 'Sitetypeoflocationofseizure_']
    variables = [col for col in all_variables if any(col.startswith(prefix) for prefix in prefixes)]
    filtered_data = data[variables]
    
    return filtered_data

def perform_clustering(filtered_data, variables):
    """
    Perform clustering on the data.

    Args:
        filtered_data (DataFrame): The DataFrame containing the filtered data.
        variables (list): The list of variables to perform clustering on, this includes "Drug class/ group", "Meansoftransportation", "Sitetypeoflocationofseizure".
        n_clusters (int): The number of clusters

    Returns:
          
    """
    
    X = filtered_data[variables]
    
    # Remove rows and columns for unavailable data
        # X = X.loc[X['']==0, :] 

    # Scale numerical features
    scaler = StandardScaler()
    X[['lat', 'lng']] = scaler.fit_transform(X[['lat', 'lng']])

    # Train the clustering model
    k = range(2, 11)
    kproto = KPrototypes(n_clusters=k, init='Cao', random_state=42)
    clusters = kproto.fit_predict(X.values, categorical=[2,3,4])

    return kproto.cluster_centroids_

if __name__ == '__main__':
    # Importing data
    data = import_data()

    # Filtering data
    filtered_data = filter_data(data)

    # Train and evaluate model
    centroids = perform_clustering(filtered_data)