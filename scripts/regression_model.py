import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error



def import_data():
    """
    Importing processed data from csv file.
    """
    data = pd.read_csv('data/processed_data.csv', header=0, low_memory=False)
    data['DateDDMMYYYY'] = pd.to_datetime(data['DateDDMMYYYY'], format='mixed')

    return data

def filter_data(data):
    """
    Filtering attributes from data used for regression model.

    Args:
        data (DataFrame): The DataFrame containing the processed data.

    Returns:
        filtered_data (DataFrame): The DataFrame containing the filtered data.
    """

    # Filtering off data with drug class, meansoftransportation, or sitetypeoflocationofseizure
    missing_data_attributes = ['Drug class/ group_Unspecified', 'Meansoftransportation_Data not available', 'Sitetypeoflocationofseizure_Data not available']
    for attribute in missing_data_attributes:
        data = data[data[attribute] != 1]
        data = data.drop(attribute, axis=1)

    # Filtering for variables of interest
    all_variables = data.columns
    prefixes = ['Drugquantity', 'lat', 'lng', 'Drug class/ group_', 'Meansoftransportation_', 'Sitetypeoflocationofseizure_']
    variables = [col for col in all_variables if any(col.startswith(prefix) for prefix in prefixes)]
    filtered_data = data[variables]
    
    # Filtering for variables with missing drug quantity
    filtered_data = filtered_data.dropna(axis=0)
    
    return filtered_data

def split_and_scale_data(filtered_data):
    """
    Performing train-test split of data and standard scaling of geospatial features.

    Args:
        filtered_data (DataFrame): The DataFrame containing the filtered data.

    Returns:
        X_train, X_test, y_train, y_test
          
    """
    # Train-test split of data
    X, y = filtered_data.drop(['Drugquantity'], axis=1), filtered_data['Drugquantity']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale geospatial features
    scaler = StandardScaler()
    scaled_train = scaler.fit_transform(X_train[['lat', 'lng']])

    X_train['lat'] = scaled_train[:, 0]
    X_train['lng'] = scaled_train[:, 1]
    
    scaled_test = scaler.transform(X_test[['lat', 'lng']])
    X_test['lat'] = scaled_test[:, 0]
    X_test['lng'] = scaled_test[:, 1]

    return X_train, X_test, y_train, y_test

def perform_regression(X_train, X_test, y_train, y_test):
    """
    Perform regression on the data.

    Args:
        filtered_data (DataFrame): The DataFrame containing the filtered data.

    Returns:
          
    """
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    print(f"MSE for linear regression model is {mean_squared_error(y_test, y_pred)}")

    ridge = Ridge()
    ridge.fit(X_train, y_train)
    y_pred = ridge.predict(X_test)
    print(f"MSE for ridge regression model is {mean_squared_error(y_test, y_pred)}")

    lasso = Lasso()
    lasso.fit(X_train, y_train)
    y_pred = lasso.predict(X_test)
    print(f"MSE for ridge regression model is {mean_squared_error(y_test, y_pred)}")
     
if __name__ == '__main__':
    # Importing data
    data = import_data()

    # Filtering data
    filtered_data = filter_data(data)

    # Split and scale data
    X_train, X_test, y_train, y_test = split_and_scale_data(filtered_data)

    # Train and evaluate model
    perform_regression(X_train, X_test, y_train, y_test)