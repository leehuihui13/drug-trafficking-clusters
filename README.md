# Drug Trafficking Analysis Project
The persistent challenge of drug trafficking and smuggling poses multifaceted threats to global security and public health. Despite extensive efforts by law enforcement agencies and international organizations, the illicit drug trade continues to thrive, leading to increased crime rates, drug addiction, and social destabilization [1]. To effectively combat this issue, it is imperative to gain comprehensive insights into the underlying patterns, trends, and dynamics of drug smuggling and trafficking activities [2].

This project applies machine learning techniques to analyze drug seizure data with the aim of identifying geographical hotspots and gaining insights into the drivers of drug trafficking activities. By processing and exploring the available data, the project aims to provide actionable insights for law enforcement agencies and policymakers to craft evidence-based policies to combat illicit drug trade and safeguard public health and security.

# Research Questions
Using clustering and regression analysis, the research questions in this project aim to provide insights into the spatial and temporal dynamics of drug trafficking, as well as the underlying factors driving these illicit activities.

The research questions are as follows:
1. What are the geographical hotspots of drug seizure activities based on the characteristics of the seizure locations?
2. Can distinct clusters of drug seizure incidents be identified based on the features such as drug type, site of seizure, and means of transportation?
3. How do variables such as drug type, city/town, site of seizure, and means of transportation affect the quantity of drugs seized?

# Data Source 
The data used for this project was sourced from the United Nations Office on Drugs and Crime (UNODC) through their Individual Drug Seizures (IDS) data collection initiative [3]. Mandated by international drug conventions, the IDS gathers information on individual drug seizure cases occurring within the national territories of Member States. These seizure cases are defined as singular interceptions or apprehensions of drugs and/or New Psychoactive Substances by Law Enforcement Agencies.

The dataset utilized in this project contains individual drug seizure cases reported to UNODC between 01.01.2011 and 31.12.2022. It encompasses the following variables - date of seizure, country of seizure, sub-region, region (continent), drug, drug quantity, specific city/town, site of seizure, and means of transportation.

The dataset is publicly available for download on the UNODC Data Portal at: https://dmp.unodc.org/downloadIDS. This is found in the data folder as `IDS-data-2011_2022-Nov23.xlsx`.
 
# Scripts
The project includes the following scripts in the scripts folder:
* `process_data.py`: Script for processing and cleaning raw data into a suitable format for analysis.
* `create_dash.py`: Script that creates a Dash web application that visualizes drug trafficking activity clusters on a map.
* `train_model.py`: Script for training machine learning models on the processed data.
* `evaluate_model.py`: Script for evaluating machine learning models.
* `run.sh`: Bash script for executing the entire pipeline, from data preprocessing to model evaluation.

# Installation
To run the scripts in this project, ensure you have Python 3 installed along with the necessary dependencies listed in requirements.txt. You can install the dependencies using the following command:
```
pip install -r requirements.txt
```

# Usage
1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Run the desired scripts from the scripts folder to process the data, perform exploratory data analysis, and train machine learning models.
4. Execute `run.sh` to automate the entire pipeline.

# Visualization
The Dash web application that visualizes drug trafficking activity clusters on a map can be found on http://leehuihui13.pythonanywhere.com/. The application allows users to select specific years and drug classes to filter the data and update the map accordingly. 

# References
[1] Merrill Singer. “Drugs and development: the global impact of drug use and trafficking on social and economic development”. In: International journal of drug policy 19.6 (2008), pp. 467–478. DOI: https://doi.org/10.1016/j.drugpo.2006.12.007. \
[2] Erik Cheekes Luca Giommoni R.V. Gundur. “International drug trafficking: past, present, and prospective trends”. In: Oxford research encyclopedia of criminology (2020). DOI: https://doi.org/10.1093/acrefore/9780190264079.013.470. \
[3] United Nations Office on Drugs and Crime. Individual drug seizures (ids) data collection. url: https://www.unodc.org/unodc/en/data-and-analysis/statistics/drugs/seizures_cases.html.