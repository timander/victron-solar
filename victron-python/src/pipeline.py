"""Main data pipeline for solar CSV ingestion and processing using Polars."""

from pathlib import Path

import polars as pl
from loguru import logger

from src.models import SolarSummary


class SolarPipeline:
    """Pipeline for processing Victron solar equipment CSV data."""

    def __init__(self, csv_path: str | Path) -> None:
        """Initialize the pipeline with a CSV file path.

        Args:
            csv_path: Path to the solar CSV data file

        Raises:
            FileNotFoundError: If the CSV file doesn't exist
        """
        self.csv_path = Path(csv_path)
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        self.df: pl.DataFrame | None = None
        logger.info(f"Initialized SolarPipeline with {self.csv_path}")

    def load(self) -> pl.DataFrame:
        """Load the solar CSV data into a Polars DataFrame.

        Returns:
            DataFrame containing the solar data

        Raises:
            ValueError: If the CSV cannot be parsed or is empty
        """
        try:
            self.df = pl.read_csv(self.csv_path, try_parse_dates=True)
            logger.info(f"Loaded {self.df.height} rows from {self.csv_path}")

            if self.df.height == 0:
                raise ValueError(f"CSV file is empty: {self.csv_path}")

            return self.df
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            raise

    def summarize(self) -> SolarSummary:
        """Return a summary of solar usage statistics.

        Returns:
            SolarSummary object with aggregated statistics

        Raises:
            RuntimeError: If data hasn't been loaded yet
        """
        if self.df is None:
            self.load()

        if self.df is None:
            raise RuntimeError("Failed to load data")

        df = self.df
        summary_data = {
            "total_yield_wh": float(df["Yield(Wh)"].sum()),
            "max_pv_power_w": float(df["Max. PV power(W)"].max()),
            "max_pv_voltage_v": float(df["Max. PV voltage(V)"].max()),
            "min_battery_voltage_v": float(df["Min. battery voltage(V)"].min()),
            "max_battery_voltage_v": float(df["Max. battery voltage(V)"].max()),
            "total_days": int(df.height),
        }

        logger.debug(f"Generated summary: {summary_data}")
        return SolarSummary(**summary_data)

    def filter_by_date(self, start: str, end: str) -> pl.DataFrame:
        """Filter records between two dates (inclusive).

        Args:
            start: Start date in MM/DD/YY format
            end: End date in MM/DD/YY format

        Returns:
            Filtered DataFrame

        Raises:
            RuntimeError: If data hasn't been loaded yet
        """
        if self.df is None:
            self.load()

        if self.df is None:
            raise RuntimeError("Failed to load data")

        mask = (self.df["Date"] >= start) & (self.df["Date"] <= end)
        filtered = self.df.filter(mask)
        logger.info(f"Filtered {filtered.height} rows between {start} and {end}")
        return filtered
