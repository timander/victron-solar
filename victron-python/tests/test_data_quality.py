import os

from src.data_quality import validate_solar_data
from src.pipeline import SolarPipeline


def test_data_quality():
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    df = pipeline.load()
    report = validate_solar_data(df)

    # Check that we ran all expected checks
    assert report.total_checks > 0

    # All checks should pass for valid data
    assert report.all_passed, f"Data quality checks failed:\n{report}"

    # Verify individual checks ran
    check_names = {r.check_name for r in report.results}
    assert "required_columns_exist" in check_names
    assert "yield_no_nulls" in check_names
    assert "yield_non_negative" in check_names
