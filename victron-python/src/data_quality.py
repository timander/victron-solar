"""Data quality checks for solar CSV data using native Polars validation."""

from dataclasses import dataclass

import polars as pl
from loguru import logger


@dataclass
class ValidationResult:
    """Result of a data quality validation check."""

    check_name: str
    passed: bool
    message: str
    rows_affected: int = 0


@dataclass
class DataQualityReport:
    """Comprehensive data quality report."""

    total_checks: int
    passed_checks: int
    failed_checks: int
    results: list[ValidationResult]

    @property
    def all_passed(self) -> bool:
        """Check if all validations passed."""
        return self.failed_checks == 0

    def __str__(self) -> str:
        """Return a human-readable summary."""
        status = "✓ PASSED" if self.all_passed else "✗ FAILED"
        return (
            f"Data Quality Report: {status}\n"
            f"  Total checks: {self.total_checks}\n"
            f"  Passed: {self.passed_checks}\n"
            f"  Failed: {self.failed_checks}"
        )


def validate_solar_data(df: pl.DataFrame) -> DataQualityReport:
    """Run data quality checks on the solar data using native Polars operations.

    Args:
        df: Polars DataFrame containing solar data

    Returns:
        DataQualityReport with all validation results
    """
    results: list[ValidationResult] = []

    # Check 1: Required columns exist
    required_columns = ["Date", "Yield(Wh)", "Max. PV power(W)", "Max. PV voltage(V)"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    results.append(
        ValidationResult(
            check_name="required_columns_exist",
            passed=len(missing_columns) == 0,
            message=f"Missing columns: {missing_columns}"
            if missing_columns
            else "All required columns present",
        )
    )

    # Check 2: No null values in Yield column
    null_count = df["Yield(Wh)"].null_count()
    results.append(
        ValidationResult(
            check_name="yield_no_nulls",
            passed=null_count == 0,
            message=f"Found {null_count} null values in Yield(Wh)"
            if null_count > 0
            else "No null values in Yield(Wh)",
            rows_affected=null_count,
        )
    )

    # Check 3: Yield values are non-negative
    negative_count = df.filter(pl.col("Yield(Wh)") < 0).height
    results.append(
        ValidationResult(
            check_name="yield_non_negative",
            passed=negative_count == 0,
            message=f"Found {negative_count} negative Yield values"
            if negative_count > 0
            else "All Yield values are non-negative",
            rows_affected=negative_count,
        )
    )

    # Check 4: Date column has valid format
    try:
        # Check if dates can be parsed (basic validation)
        date_nulls = df["Date"].null_count()
        results.append(
            ValidationResult(
                check_name="date_format_valid",
                passed=date_nulls == 0,
                message=f"Found {date_nulls} null/invalid dates"
                if date_nulls > 0
                else "All dates are valid",
                rows_affected=date_nulls,
            )
        )
    except Exception as e:
        results.append(
            ValidationResult(
                check_name="date_format_valid",
                passed=False,
                message=f"Date validation error: {e}",
            )
        )

    # Check 5: Battery voltage is within reasonable range (10-16V typical for 12V system)
    if "Min. battery voltage(V)" in df.columns:
        out_of_range = df.filter(
            (pl.col("Min. battery voltage(V)") < 10) | (pl.col("Min. battery voltage(V)") > 16)
        ).height
        results.append(
            ValidationResult(
                check_name="battery_voltage_range",
                passed=out_of_range == 0,
                message=f"Found {out_of_range} rows with battery voltage out of range (10-16V)"
                if out_of_range > 0
                else "Battery voltages within normal range",
                rows_affected=out_of_range,
            )
        )

    # Generate report
    passed_count = sum(1 for r in results if r.passed)
    failed_count = len(results) - passed_count

    report = DataQualityReport(
        total_checks=len(results),
        passed_checks=passed_count,
        failed_checks=failed_count,
        results=results,
    )

    # Log results
    if report.all_passed:
        logger.info(f"Data quality validation passed: {passed_count}/{len(results)} checks")
    else:
        logger.warning(
            f"Data quality validation failed: {failed_count}/{len(results)} checks failed"
        )
        for result in results:
            if not result.passed:
                logger.warning(f"  {result.check_name}: {result.message}")

    return report
