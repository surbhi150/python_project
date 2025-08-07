import pandas as pd
import os

# Define the path to your data folder
script_dir = os.path.dirname(__file__)
data_folder_path = os.path.join(script_dir, 'data')

# Ensure the data folder exists
if not os.path.exists(data_folder_path):
    print(f"Error: Data folder not found at '{data_folder_path}'")
    exit()

# Construct the full path to the CSV file
bike_csv_path = os.path.join(data_folder_path, 'final dataset.csv')

try:
    bike_features_df = pd.read_csv(bike_csv_path, encoding='utf-8')
    print("CSV loaded successfully!")
except:
    print("An error occurred while loading the file ")    
