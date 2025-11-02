import pytest
from src.pipeline import SolarPipeline
from src.visualization import plot_yield_over_time

def test_plot_yield_over_time(tmp_path):
    pipeline = SolarPipeline()
    df = pipeline.load()
    save_path = tmp_path / "yield_plot.png"
    plot_yield_over_time(df, str(save_path))
    assert save_path.exists()
