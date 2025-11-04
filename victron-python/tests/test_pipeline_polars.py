import os

from src.pipeline import SolarPipeline


def test_pipeline_load_and_summary():
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    df = pipeline.load()
    assert df.height > 0
    summary = pipeline.summarize()
    assert "total_yield_Wh" in summary
    assert summary["total_days"] == df.height


def test_pipeline_filter_by_date():
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    pipeline.load()
    filtered = pipeline.filter_by_date("10/10/25", "10/12/25")
    assert all(filtered["Date"] >= "10/10/25")
    assert all(filtered["Date"] <= "10/12/25")
