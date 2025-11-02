import pytest
from src.pipeline import SolarPipeline

def test_pipeline_load_and_summary():
    pipeline = SolarPipeline()
    df = pipeline.load()
    assert df.height > 0
    summary = pipeline.summarize()
    assert "total_yield_Wh" in summary
    assert summary["total_days"] == df.height

def test_pipeline_filter_by_date():
    pipeline = SolarPipeline()
    pipeline.load()
    filtered = pipeline.filter_by_date("10/10/25", "10/12/25")
    assert all(filtered["Date"] >= "10/10/25")
    assert all(filtered["Date"] <= "10/12/25")
