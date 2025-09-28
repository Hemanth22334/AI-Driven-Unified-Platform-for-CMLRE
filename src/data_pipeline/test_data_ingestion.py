import os
import pandas as pd
import pytest
from data_ingestion import ingest_oceanography_data

@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing."""
    data = {
        'temperature_F': [68, 50, 77],
        'salinity': [35, 45, -5],
        'pressure': [10, 12, 15]
    }
    df = pd.DataFrame(data)
    file_path = "test_data.csv"
    df.to_csv(file_path, index=False)
    yield file_path
    os.remove(file_path)

def test_ingest_oceanography_data(sample_csv_file):
    """Test the ingest_oceanography_data function."""
    df, flagged_rows = ingest_oceanography_data(sample_csv_file)

    # Test column renaming
    expected_columns = ['water_temperature_C', 'salinity_PSU', 'pressure_db']
    assert all(col in df.columns for col in expected_columns)

    # Test temperature conversion
    assert df['water_temperature_C'][0] == 20.0
    assert df['water_temperature_C'][1] == 10.0
    assert df['water_temperature_C'][2] == 25.0

    # Test salinity flagging
    assert len(flagged_rows) == 2
    assert flagged_rows[0]['row_index'] == 1
    assert flagged_rows[0]['reason'] == "Invalid salinity: 45.0"
    assert flagged_rows[1]['row_index'] == 2
    assert flagged_rows[1]['reason'] == "Invalid salinity: -5.0"

def test_file_not_found():
    """Test that FileNotFoundError is raised for a non-existent file."""
    with pytest.raises(FileNotFoundError):
        ingest_oceanography_data("non_existent_file.csv")