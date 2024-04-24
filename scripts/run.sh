#!/bin/bash

# Clean & process data
python scripts/process_data.py

# Explore data
python scripts/create_dash.py

# Train model
python scripts/train_model.py

# Visualize data
python scripts/evaluate_model.py