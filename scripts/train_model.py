import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

# TODO: kmeans_cluster
# TODO: DBSCAN clustering
# TODO: Calculate silhouette_score

def import_data():
    """
    Importing processed data from csv file.
    """
    data = pd.read_csv('data/processed_data.csv', header=0, low_memory=False)

    return data

def perform_kmeans_clustering(data):
    """
    Perform K-Means clustering on the data.

    Args:
        data (DataFrame): The DataFrame containing the processed data.

    Returns:
          
    """
    columns = [col for col in data.columns if 'Drug class/ group_' in col]
    columns.extend(['lat', 'lng'])
    X = data.loc[:, columns]
    kmeans = KMeans(n_clusters=10, random_state=42, n_init="auto")

    return 



### -> data.groupby(data['DateDDMMYYYY'].dt.year,data['DateDDMMYYYY'].dt.month)['DateDDMMYYYY'].agg('count') 

