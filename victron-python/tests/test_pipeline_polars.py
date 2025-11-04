import os

from src.pipeline import SolarPipeline


def test_pipeline_load_and_summary():
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    df = pipeline.load()
    assert df.height > 0

    # Test that summarize returns a typed SolarSummary object
    summary = pipeline.summarize()
    assert hasattr(summary, "total_yield_wh")
    assert hasattr(summary, "total_days")
    assert summary.total_yield_wh > 0
    assert summary.total_days == df.height
    assert summary.max_pv_power_w >= 0
    assert summary.min_battery_voltage_v > 0


def test_pipeline_filter_by_date():
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    pipeline.load()
    filtered = pipeline.filter_by_date("10/10/25", "10/12/25")
    assert all(filtered["Date"] >= "10/10/25")
    assert all(filtered["Date"] <= "10/12/25")
