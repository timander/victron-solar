import os

from src.pipeline import SolarPipeline
from src.visualization import close_all_figures, plot_battery_voltage, plot_yield_over_time


def test_plot_yield_over_time(tmp_path):
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    df = pipeline.load()
    save_path = tmp_path / "yield_plot.png"

    fig = plot_yield_over_time(df, str(save_path))
    assert save_path.exists()
    assert fig is not None

    # Clean up
    close_all_figures()


def test_plot_battery_voltage(tmp_path):
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    df = pipeline.load()
    save_path = tmp_path / "battery_plot.png"

    fig = plot_battery_voltage(df, str(save_path))
    assert save_path.exists()
    assert fig is not None

    # Clean up
    close_all_figures()
