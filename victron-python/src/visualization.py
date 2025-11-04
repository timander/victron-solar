"""Visualization utilities for solar usage summary report."""

from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl
from loguru import logger
from matplotlib.figure import Figure


def plot_yield_over_time(df: pl.DataFrame, save_path: str | Path | None = None) -> Figure:
    """Plot daily solar yield over time.

    Args:
        df: DataFrame containing solar data with Date and Yield(Wh) columns
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object

    Raises:
        ValueError: If required columns are missing
    """
    required_cols = ["Date", "Yield(Wh)"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    dates = df["Date"].to_list()
    yields = df["Yield(Wh)"].to_list()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, yields, marker="o", linestyle="-", linewidth=2, markersize=4)
    ax.set_title("Daily Solar Yield Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Yield (Wh)", fontsize=12)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if save_path:
        save_path = Path(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        logger.info(f"Saved visualization to {save_path}")
    else:
        plt.show()

    return fig


def plot_battery_voltage(df: pl.DataFrame, save_path: str | Path | None = None) -> Figure:
    """Plot battery voltage range over time.

    Args:
        df: DataFrame containing solar data with battery voltage columns
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object

    Raises:
        ValueError: If required columns are missing
    """
    required_cols = ["Date", "Min. battery voltage(V)", "Max. battery voltage(V)"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    dates = df["Date"].to_list()
    min_voltage = df["Min. battery voltage(V)"].to_list()
    max_voltage = df["Max. battery voltage(V)"].to_list()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, min_voltage, label="Min Voltage", marker="v", linestyle="-", linewidth=2)
    ax.plot(dates, max_voltage, label="Max Voltage", marker="^", linestyle="-", linewidth=2)
    ax.fill_between(dates, min_voltage, max_voltage, alpha=0.2)
    ax.set_title("Battery Voltage Range Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Voltage (V)", fontsize=12)
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if save_path:
        save_path = Path(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        logger.info(f"Saved visualization to {save_path}")
    else:
        plt.show()

    return fig


def close_all_figures() -> None:
    """Close all matplotlib figures to free memory."""
    plt.close("all")
    logger.debug("Closed all matplotlib figures")
