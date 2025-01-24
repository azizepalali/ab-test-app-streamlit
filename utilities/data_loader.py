import pandas as pd

def load_default_data(filepath="data/ab_data.csv"):
    """
    Loads the default A/B test dataset.
    
    Parameters:
        filepath (str): Path to the default CSV file.
    
    Returns:
        pd.DataFrame: Default A/B test data.
    """
    return pd.read_csv(filepath)