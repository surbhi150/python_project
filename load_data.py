# utils/load_data.py

import pandas as pd

def load_data(file_path="final_dataset.csv"):
    """
    Loads and cleans the health center CSV data.

    - Strips and standardizes column names.
    - Raises informative exceptions.
    """
    try:
        df = pd.read_csv(file_path)

        # Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.replace(r'\s+', '_', regex=True)
            .str.replace(r'[^\w]', '', regex=True)
        )

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"❌ File is empty: {file_path}")
    except Exception as e:
        raise Exception(f"❌ Failed to load data: {e}")
