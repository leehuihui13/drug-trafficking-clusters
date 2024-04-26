#!/bin/bash

# Clean & process data
python scripts/process_data.py

# Explore data
python scripts/create_dash.py

# Train and evaluate model
python scripts/train_model.py

# Visualize model
python scripts/visualize_model.py