"""Data quality checks for solar CSV data using Great Expectations."""
import great_expectations as ge
import polars as pl
from pathlib import Path


def validate_solar_data(df: pl.DataFrame) -> dict:
    """
    Run data quality checks on the solar data using Great Expectations.
    Returns a dictionary with validation results.
    """
    # Convert Polars DataFrame to Pandas for GE compatibility
    pd_df = df.to_pandas()
    ge_df = ge.from_pandas(pd_df)

    # Example expectations (customize as needed)
    results = {}
    results['expect_column_to_exist'] = ge_df.expect_column_to_exist("Yield(Wh)").success
    results['expect_column_values_to_not_be_null'] = ge_df.expect_column_values_to_not_be_null("Yield(Wh)").success
    results['expect_column_values_to_be_between'] = ge_df.expect_column_values_to_be_between(
        "Yield(Wh)", min_value=0, max_value=None
    ).success
    results['expect_column_values_to_not_be_null_date'] = ge_df.expect_column_values_to_not_be_null("Date").success
    results['expect_column_values_to_match_strftime_format'] = ge_df.expect_column_values_to_match_strftime_format(
        "Date", "%m/%d/%y"
    ).success
    return results
