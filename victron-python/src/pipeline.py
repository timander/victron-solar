"""Main data pipeline for solar CSV ingestion and processing using Polars."""
from pathlib import Path
import polars as pl
from typing import Optional

class SolarPipeline:
    def __init__(self, csv_path: Optional[str] = None):
        self.csv_path = csv_path or str(Path(__file__).parent.parent / "data" / "SolarHistory.csv")
        self.df: Optional[pl.DataFrame] = None

    def load(self) -> pl.DataFrame:
        """Load the solar CSV data into a Polars DataFrame."""
        self.df = pl.read_csv(self.csv_path, try_parse_dates=True)
        return self.df

    def summarize(self) -> dict:
        """Return a summary of solar usage statistics."""
        if self.df is None:
            self.load()
        df = self.df
        summary = {
            "total_yield_Wh": df["Yield(Wh)"].sum(),
            "max_pv_power_W": df["Max. PV power(W)"].max(),
            "max_pv_voltage_V": df["Max. PV voltage(V)"].max(),
            "min_battery_voltage_V": df["Min. battery voltage(V)"].min(),
            "max_battery_voltage_V": df["Max. battery voltage(V)"].max(),
            "total_days": df.height,
        }
        return summary

    def filter_by_date(self, start: str, end: str) -> pl.DataFrame:
        """Filter records between two dates (inclusive). Dates in MM/DD/YY format."""
        if self.df is None:
            self.load()
        mask = (self.df["Date"] >= start) & (self.df["Date"] <= end)
        return self.df.filter(mask)
