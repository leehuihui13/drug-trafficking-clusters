#!/bin/bash

# Clean & process data
python scripts/process_data.py

# Explore data
python scripts/eda.py

# Train model
python scripts/train_model.py

# Visualize data
python scripts/visualize_model.py