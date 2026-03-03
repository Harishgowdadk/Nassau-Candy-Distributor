import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    return df


def preprocess_data(df):

    # Convert Dates (DD-MM-YYYY)
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

    # Create Lead Time
    df['Lead_Time'] = (df['Ship Date'] - df['Order Date']).dt.days

    # Remove invalid values
    df = df[df['Lead_Time'] >= 0]

    return df
