import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask




# Initialize figure
data = pd.read_csv('data/processed_data.csv', header=0, low_memory=False)
data['DateDDMMYYYY'] = pd.to_datetime(data['DateDDMMYYYY'], format='mixed')

# Create Dash app
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Define layout for main page
app.layout = html.Div([
    html.H1("Drug Trafficking Activity Clusters"),

    html.Label("Select Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in data['DateDDMMYYYY'].dt.year.unique()],
        value=[],  # Default selection set to all available years
        multi=True  # Allow multiple selections
    ),

    html.Label("Select Drug Class:"),
    dcc.Dropdown(
        id='drug-class-dropdown',
        options=[{'label': drug_class, 'value': drug_class} for drug_class in data['Drug class/ group'].unique()],
        value=[],  # Default selection set to all available drug classes
        multi=True  # Allow multiple selections
    ),
    dcc.Graph(id='map', style={'width': '100%', 'height': 'calc(100vh - 150px)'})
])

# Define callback to update the map
@app.callback(
    Output('map', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('drug-class-dropdown', 'value')]
)

def update_map(selected_years, selected_drug_classes):
    filtered_data = data
    if selected_years:
        filtered_data = filtered_data[filtered_data['DateDDMMYYYY'].dt.year.isin(selected_years)]
    if selected_drug_classes:
        filtered_data = filtered_data[filtered_data['Drug class/ group'].isin(selected_drug_classes)]

    # Calculate count of seizures per country
    seizure_counts = filtered_data.groupby(['Countryofseizure', 'lat', 'lng']).size().reset_index(name='seizure_count')    
    
    # Plotly express scatter mapbox plot with marker size based on seizure count and marker color based on continent
    fig = px.scatter_mapbox(seizure_counts, 
                            lat='lat', lon='lng', 
                            hover_name='Countryofseizure',
                            # color='continent', color_discrete_sequence=px.colors.qualitative.Pastel, 
                            zoom=1,
                            size='seizure_count', 
                            size_max=100)
    fig.update_layout(mapbox_style='carto-positron')
    fig.update_layout(margin={'r':0,'t':0,'l':0,"b":0})
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')

