import os
from src.pipeline import SolarPipeline
from src.data_quality import validate_solar_data

def test_data_quality():
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    df = pipeline.load()
    results = validate_solar_data(df)
    # All checks should pass for a valid file
    assert all(results.values()), f"Data quality checks failed: {results}"
