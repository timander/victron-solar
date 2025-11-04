"""Tests for cost analysis module."""

from pathlib import Path

import polars as pl
import pytest

from src.cost_analysis import format_cost_report, generate_cost_report, save_cost_report


def test_generate_cost_report():
    """Test cost report generation with sample data."""
    df = pl.DataFrame(
        {
            "Yield(Wh)": [100, 200, 150, 250],
            "Consumption(Wh)": [50, 75, 100, 80],
        }
    )

    report = generate_cost_report(df, rate_per_kwh=0.14)

    assert report.total_solar_kwh == 0.7  # 700 Wh = 0.7 kWh
    assert report.total_consumption_kwh == 0.305  # 305 Wh = 0.305 kWh
    assert report.solar_value_usd == pytest.approx(0.098, abs=0.001)  # 0.7 * 0.14
    assert report.consumption_cost_usd == pytest.approx(0.0427, abs=0.001)  # 0.305 * 0.14
    assert report.net_savings_usd == pytest.approx(0.0553, abs=0.001)
    assert report.solar_offset_percent == pytest.approx(229.5, abs=0.1)  # 0.7/0.305 * 100
    assert report.days_analyzed == 4
    assert report.rate_per_kwh == 0.14


def test_generate_cost_report_no_consumption():
    """Test cost report when consumption is zero."""
    df = pl.DataFrame(
        {
            "Yield(Wh)": [100, 200, 150],
            "Consumption(Wh)": [0, 0, 0],
        }
    )

    report = generate_cost_report(df, rate_per_kwh=0.14)

    assert report.total_solar_kwh == 0.45
    assert report.total_consumption_kwh == 0
    assert report.solar_offset_percent == 0  # Division by zero handled
    assert report.net_savings_usd == pytest.approx(0.063, abs=0.001)


def test_generate_cost_report_missing_columns():
    """Test cost report raises error for missing columns."""
    df = pl.DataFrame(
        {
            "Yield(Wh)": [100, 200],
        }
    )

    with pytest.raises(ValueError, match="must contain"):
        generate_cost_report(df)


def test_format_cost_report():
    """Test cost report formatting."""
    df = pl.DataFrame(
        {
            "Yield(Wh)": [1000, 2000, 1500],
            "Consumption(Wh)": [500, 750, 600],
        }
    )

    report = generate_cost_report(df, rate_per_kwh=0.14)
    formatted = format_cost_report(report)

    assert "SOLAR ENERGY COST ANALYSIS REPORT" in formatted
    assert "4.50 kWh" in formatted  # Total solar
    assert "1.85 kWh" in formatted  # Total consumption
    assert "0.63" in formatted  # Solar value
    assert "0.26" in formatted  # Consumption cost
    assert "Analysis Period: 3 days" in formatted
    assert "Electricity Rate: $0.140 per kWh" in formatted


def test_save_cost_report(tmp_path: Path):
    """Test saving cost report to file."""
    df = pl.DataFrame(
        {
            "Yield(Wh)": [1000, 2000, 1500],
            "Consumption(Wh)": [500, 750, 600],
        }
    )

    output_file = tmp_path / "cost_report.txt"
    save_cost_report(df, output_file, rate_per_kwh=0.14)

    assert output_file.exists()
    content = output_file.read_text()
    assert "SOLAR ENERGY COST ANALYSIS REPORT" in content
    assert "4.50 kWh" in content
