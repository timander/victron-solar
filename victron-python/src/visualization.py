"""Visualization utilities for solar usage summary report."""
import matplotlib.pyplot as plt
import polars as pl

def plot_yield_over_time(df: pl.DataFrame, save_path: str = None):
    """Plot daily solar yield over time."""
    dates = df["Date"].to_list()
    yields = df["Yield(Wh)"].to_list()
    plt.figure(figsize=(10, 5))
    plt.plot(dates, yields, marker="o", linestyle="-")
    plt.title("Daily Solar Yield Over Time")
    plt.xlabel("Date")
    plt.ylabel("Yield (Wh)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()