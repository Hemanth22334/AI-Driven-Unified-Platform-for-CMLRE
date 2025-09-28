import pandas as pd
from typing import Tuple, List

def ingest_oceanography_data(file_path: str) -> Tuple[pd.DataFrame, List[dict]]:
    """
    Reads oceanographic data from a CSV file, standardizes it, and flags invalid rows.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Tuple[pd.DataFrame, List[dict]]: A tuple containing:
            - A pandas DataFrame with the standardized data.
            - A list of dictionaries, where each dictionary represents a flagged row
              and includes the original row data and a reason for flagging.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at: {file_path}")

    flagged_rows = []

    # Standardize column names
    column_mapping = {
        'temperature_F': 'water_temperature_C',
        'salinity': 'salinity_PSU',
        'pressure': 'pressure_db'
    }
    df.rename(columns=column_mapping, inplace=True)

    # Convert temperature from Fahrenheit to Celsius
    if 'water_temperature_C' in df.columns:
        df['water_temperature_C'] = (df['water_temperature_C'] - 32) * 5.0/9.0

    # Validate salinity and flag rows
    if 'salinity_PSU' in df.columns:
        for index, row in df.iterrows():
            salinity = row['salinity_PSU']
            if not (0 <= salinity <= 40):
                flagged_rows.append({
                    'row_index': index,
                    'data': row.to_dict(),
                    'reason': f"Invalid salinity: {salinity}"
                })

    return df, flagged_rows