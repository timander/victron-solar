"""Comprehensive visualization utilities for Victron MPPT solar charge controller analysis."""

from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl
from loguru import logger
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec


def create_comprehensive_dashboard(df: pl.DataFrame, save_path: str | Path | None = None) -> Figure:
    """Create a comprehensive solar system performance dashboard.

    This multi-panel dashboard provides key insights for understanding:
    - Energy production trends and efficiency
    - Battery health and state of charge
    - Solar panel performance and power output
    - MPPT charging behavior (bulk/absorption/float phases)
    - System health indicators

    Args:
        df: DataFrame containing Victron MPPT history data
        save_path: Optional path to save the dashboard

    Returns:
        matplotlib Figure object with comprehensive dashboard

    Raises:
        ValueError: If required columns are missing
    """
    logger.info("Creating comprehensive solar dashboard")

    # Sort by Days ago (descending = oldest first, since days ago is inverse chronological)
    df = df.sort("Days ago", descending=True)
    dates = df["Date"].to_list()

    # Create figure with custom layout
    fig = plt.figure(figsize=(20, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

    # Panel 1: Daily Energy Yield (top left, spans 2 columns)
    ax1 = fig.add_subplot(gs[0, :2])
    yields = df["Yield(Wh)"].to_list()
    avg_yield = df["Yield(Wh)"].mean()
    ax1.bar(dates, yields, alpha=0.7, color="gold", edgecolor="orange", linewidth=1.5)
    ax1.axhline(
        avg_yield, color="red", linestyle="--", linewidth=2, label=f"Avg: {avg_yield:.0f} Wh"
    )
    ax1.set_title("Daily Solar Energy Production", fontsize=14, fontweight="bold", pad=10)
    ax1.set_ylabel("Energy Yield (Wh)", fontsize=11)
    ax1.tick_params(axis="x", rotation=45, labelsize=9)
    ax1.grid(True, alpha=0.3, axis="y")
    ax1.legend(loc="upper right")

    # Panel 2: Summary Statistics (top right)
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.axis("off")
    total_yield = df["Yield(Wh)"].sum()
    max_power = df["Max. PV power(W)"].max()
    avg_max_voltage = df["Max. battery voltage(V)"].mean()
    min_min_voltage = df["Min. battery voltage(V)"].min()
    days = df.height

    summary_text = f"""
    SYSTEM SUMMARY ({days} days)

    Total Energy: {total_yield:.0f} Wh
    Daily Average: {avg_yield:.0f} Wh
    Peak Power: {max_power:.0f} W

    BATTERY HEALTH
    Max Voltage: {avg_max_voltage:.2f} V
    Min Voltage: {min_min_voltage:.2f} V
    Status: {"Healthy" if min_min_voltage > 12.0 else "Low voltage detected"}

    {"WARNING: Battery may be undercharged\nor oversized for solar capacity" if total_yield < 500 else "System operating normally"}
    """
    ax2.text(
        0.05,
        0.95,
        summary_text,
        transform=ax2.transAxes,
        fontsize=11,
        verticalalignment="top",
        fontfamily="monospace",
        bbox={"boxstyle": "round", "facecolor": "wheat", "alpha": 0.3},
    )

    # Panel 3: Battery Voltage Range (middle left)
    ax3 = fig.add_subplot(gs[1, 0])
    min_v = df["Min. battery voltage(V)"].to_list()
    max_v = df["Max. battery voltage(V)"].to_list()
    ax3.fill_between(
        range(len(dates)), min_v, max_v, alpha=0.3, color="green", label="Voltage Range"
    )
    ax3.plot(
        min_v, "v-", color="darkred", linewidth=2, markersize=4, label="Min (Depth of Discharge)"
    )
    ax3.plot(max_v, "^-", color="darkgreen", linewidth=2, markersize=4, label="Max (Charged)")
    ax3.axhline(14.4, color="blue", linestyle="--", alpha=0.5, label="Absorption setpoint")
    ax3.axhline(13.5, color="orange", linestyle="--", alpha=0.5, label="Float setpoint")
    ax3.axhline(12.0, color="red", linestyle="--", alpha=0.5, label="Low battery warning")
    ax3.set_title("Battery Voltage Behavior", fontsize=12, fontweight="bold")
    ax3.set_ylabel("Voltage (V)", fontsize=10)
    ax3.set_xlabel("Days", fontsize=10)
    ax3.legend(fontsize=8, loc="lower left")
    ax3.grid(True, alpha=0.3)

    # Panel 4: Solar Panel Performance (middle center)
    ax4 = fig.add_subplot(gs[1, 1])
    pv_power = df["Max. PV power(W)"].to_list()
    pv_voltage = df["Max. PV voltage(V)"].to_list()
    ax4_twin = ax4.twinx()

    line1 = ax4.plot(pv_power, "o-", color="orange", linewidth=2, markersize=5, label="Peak Power")
    ax4.set_ylabel("Peak PV Power (W)", fontsize=10, color="orange")
    ax4.tick_params(axis="y", labelcolor="orange")

    line2 = ax4_twin.plot(
        pv_voltage, "s-", color="blue", linewidth=2, markersize=4, alpha=0.7, label="Peak Voltage"
    )
    ax4_twin.set_ylabel("Peak PV Voltage (V)", fontsize=10, color="blue")
    ax4_twin.tick_params(axis="y", labelcolor="blue")

    ax4.set_title("Solar Panel Output", fontsize=12, fontweight="bold")
    ax4.set_xlabel("Days", fontsize=10)
    ax4.grid(True, alpha=0.3)

    # Combine legends
    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax4.legend(lines, labels, fontsize=8, loc="upper left")

    # Panel 5: Charging Phase Distribution (middle right)
    ax5 = fig.add_subplot(gs[1, 2])
    bulk_time = df["Time in bulk(m)"].to_list()
    absorption_time = df["Time in absorption(m)"].to_list()
    float_time = df["Time in float(m)"].to_list()

    x = range(len(dates))
    ax5.bar(x, bulk_time, label="Bulk", color="red", alpha=0.7)
    ax5.bar(x, absorption_time, bottom=bulk_time, label="Absorption", color="yellow", alpha=0.7)

    # Stack float on top
    bulk_abs = [b + a for b, a in zip(bulk_time, absorption_time, strict=False)]
    ax5.bar(x, float_time, bottom=bulk_abs, label="Float", color="green", alpha=0.7)

    ax5.set_title("MPPT Charging Phases", fontsize=12, fontweight="bold")
    ax5.set_ylabel("Time (minutes)", fontsize=10)
    ax5.set_xlabel("Days", fontsize=10)
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3, axis="y")

    # Panel 6: Cumulative Energy Production (bottom left)
    ax6 = fig.add_subplot(gs[2, 0])
    cumulative_yield = df["Yield(Wh)"].cum_sum().to_list()
    ax6.plot(cumulative_yield, linewidth=3, color="darkgreen", marker="o", markersize=3)
    ax6.fill_between(range(len(cumulative_yield)), cumulative_yield, alpha=0.2, color="green")
    ax6.set_title("Cumulative Energy Production", fontsize=12, fontweight="bold")
    ax6.set_ylabel("Total Energy (Wh)", fontsize=10)
    ax6.set_xlabel("Days", fontsize=10)
    ax6.grid(True, alpha=0.3)

    # Panel 7: Efficiency Metrics (bottom center)
    ax7 = fig.add_subplot(gs[2, 1])
    # Calculate charging efficiency: yield vs time spent charging
    total_charge_time = [b + a for b, a in zip(bulk_time, absorption_time, strict=False)]
    efficiency = [
        y / (t / 60) if t > 0 else 0 for y, t in zip(yields, total_charge_time, strict=False)
    ]  # Wh per hour

    ax7.plot(efficiency, "o-", color="purple", linewidth=2, markersize=5)
    ax7.axhline(
        sum(efficiency) / len(efficiency),
        color="red",
        linestyle="--",
        label=f"Avg: {sum(efficiency) / len(efficiency):.1f} W",
    )
    ax7.set_title("Charging Efficiency", fontsize=12, fontweight="bold")
    ax7.set_ylabel("Average Power (W)", fontsize=10)
    ax7.set_xlabel("Days", fontsize=10)
    ax7.legend(fontsize=9)
    ax7.grid(True, alpha=0.3)

    # Panel 8: Performance Insights (bottom right)
    ax8 = fig.add_subplot(gs[2, 2])
    ax8.axis("off")

    # Calculate insights
    days_low_production = sum(1 for y in yields if y < avg_yield * 0.5)
    days_good_production = sum(1 for y in yields if y > avg_yield)
    avg_bulk_time = sum(bulk_time) / len(bulk_time)
    avg_absorption_time = sum(absorption_time) / len(absorption_time)
    low_battery_days = sum(1 for v in min_v if v < 12.2)

    insights_text = f"""
    KEY INSIGHTS

    PRODUCTION
    - {days_good_production}/{days} days above average
    - {days_low_production} low production days

    CHARGING PATTERN
    - Bulk: {avg_bulk_time:.0f} min avg
    - Absorption: {avg_absorption_time:.0f} min avg
    {"- WARNING: Long bulk times suggest\n  undersized solar array" if avg_bulk_time > 300 else "- Good charging speed"}

    BATTERY HEALTH
    {"- WARNING: " + str(low_battery_days) + " days below 12.2V\n  (50% SOC for 12V system)" if low_battery_days > 0 else "- Good voltage maintained"}

    RECOMMENDATIONS
    {"- Consider larger solar array\n- Check battery capacity" if avg_yield < 200 else "- System performing well\n- Monitor during winter"}
    """

    ax8.text(
        0.05,
        0.95,
        insights_text,
        transform=ax8.transAxes,
        fontsize=10,
        verticalalignment="top",
        fontfamily="monospace",
        bbox={"boxstyle": "round", "facecolor": "lightblue", "alpha": 0.3},
    )

    # Overall title
    fig.suptitle(
        "Victron MPPT Solar Charge Controller - Performance Dashboard",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    if save_path:
        save_path = Path(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        logger.info(f"Saved comprehensive dashboard to {save_path}")
    else:
        plt.show()

    return fig


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
