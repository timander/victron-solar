"""Cost analysis module for solar energy savings calculations."""

from dataclasses import dataclass
from pathlib import Path

import polars as pl
from loguru import logger


@dataclass
class CostReport:
    """Solar energy cost analysis report."""

    total_solar_kwh: float
    total_consumption_kwh: float
    solar_value_usd: float
    consumption_cost_usd: float
    net_savings_usd: float
    solar_offset_percent: float
    days_analyzed: int
    rate_per_kwh: float
    avg_daily_solar_kwh: float
    avg_daily_consumption_kwh: float
    projected_annual_savings_usd: float


def generate_cost_report(df: pl.DataFrame, rate_per_kwh: float = 0.14) -> CostReport:
    """Generate financial analysis of solar energy savings.

    Args:
        df: Polars DataFrame with solar data (must include Yield(Wh) and Consumption(Wh))
        rate_per_kwh: Electricity rate in USD per kilowatt-hour (default: $0.14/kWh)

    Returns:
        CostReport with detailed financial analysis

    Raises:
        ValueError: If required columns are missing
    """
    required_cols = ["Yield(Wh)", "Consumption(Wh)"]
    if not all(col in df.columns for col in required_cols):
        msg = f"DataFrame must contain {required_cols}"
        raise ValueError(msg)

    logger.info(f"Generating cost report with rate ${rate_per_kwh:.3f}/kWh")

    # Convert Wh to kWh
    total_solar_wh = df["Yield(Wh)"].sum()
    total_consumption_wh = df["Consumption(Wh)"].sum()
    total_solar_kwh = total_solar_wh / 1000
    total_consumption_kwh = total_consumption_wh / 1000

    # Calculate costs
    solar_value_usd = total_solar_kwh * rate_per_kwh
    consumption_cost_usd = total_consumption_kwh * rate_per_kwh
    net_savings_usd = solar_value_usd - consumption_cost_usd

    # Calculate offset percentage
    solar_offset_percent = (
        (total_solar_kwh / total_consumption_kwh * 100) if total_consumption_kwh > 0 else 0
    )

    # Daily averages
    days = df.height
    avg_daily_solar_kwh = total_solar_kwh / days if days > 0 else 0
    avg_daily_consumption_kwh = total_consumption_kwh / days if days > 0 else 0

    # Project annual savings
    projected_annual_savings_usd = net_savings_usd * (365 / days) if days > 0 else 0

    report = CostReport(
        total_solar_kwh=total_solar_kwh,
        total_consumption_kwh=total_consumption_kwh,
        solar_value_usd=solar_value_usd,
        consumption_cost_usd=consumption_cost_usd,
        net_savings_usd=net_savings_usd,
        solar_offset_percent=solar_offset_percent,
        days_analyzed=days,
        rate_per_kwh=rate_per_kwh,
        avg_daily_solar_kwh=avg_daily_solar_kwh,
        avg_daily_consumption_kwh=avg_daily_consumption_kwh,
        projected_annual_savings_usd=projected_annual_savings_usd,
    )

    logger.info(f"Cost report generated: ${net_savings_usd:.2f} net savings over {days} days")
    return report


def format_cost_report(report: CostReport) -> str:
    """Format cost report as human-readable text.

    Args:
        report: CostReport to format

    Returns:
        Formatted multi-line string report
    """
    return f"""
{"=" * 70}
SOLAR ENERGY COST ANALYSIS REPORT
{"=" * 70}

Analysis Period: {report.days_analyzed} days
Electricity Rate: ${report.rate_per_kwh:.3f} per kWh

{"-" * 70}
ENERGY SUMMARY
{"-" * 70}
Solar Energy Collected:    {report.total_solar_kwh:>10.2f} kWh
Energy Consumed:           {report.total_consumption_kwh:>10.2f} kWh
Solar Offset:              {report.solar_offset_percent:>10.1f}%

Daily Average Solar:       {report.avg_daily_solar_kwh:>10.3f} kWh
Daily Average Consumption: {report.avg_daily_consumption_kwh:>10.3f} kWh

{"-" * 70}
FINANCIAL ANALYSIS
{"-" * 70}
Value of Solar Generated:  ${report.solar_value_usd:>10.2f}
Cost of Energy Consumed:   ${report.consumption_cost_usd:>10.2f}
NET SAVINGS:               ${report.net_savings_usd:>10.2f}

{"-" * 70}
PROJECTIONS
{"-" * 70}
Projected Annual Savings:  ${report.projected_annual_savings_usd:>10.2f}

{"-" * 70}
INVESTMENT GUIDANCE
{"-" * 70}
Based on your {report.days_analyzed}-day analysis:

• Your solar system generates ${report.solar_value_usd:.2f} worth of energy
• {"You are NET POSITIVE - solar exceeds consumption!" if report.net_savings_usd > 0 else "You are consuming more than you generate"}
• Solar offsets {report.solar_offset_percent:.1f}% of your energy needs

Annual Value Analysis:
• Annual solar generation value: ${report.projected_annual_savings_usd:.2f}
• Break-even timeline depends on system cost
  - $1,000 system = {1000 / report.projected_annual_savings_usd:.1f} years payback
  - $2,000 system = {2000 / report.projected_annual_savings_usd:.1f} years payback
  - $3,000 system = {3000 / report.projected_annual_savings_usd:.1f} years payback

{"Recommendation: Your current solar output is LOW. Consider expanding your" if report.avg_daily_solar_kwh < 0.5 else "Recommendation: Strong solar performance. Current capacity appears adequate for"}
solar array to maximize ROI and reduce grid dependence.

{"=" * 70}
"""


def save_cost_report(df: pl.DataFrame, output_path: Path | str, rate_per_kwh: float = 0.14) -> None:
    """Generate and save cost report to file.

    Args:
        df: Polars DataFrame with solar data
        output_path: Path to save the text report
        rate_per_kwh: Electricity rate in USD per kilowatt-hour (default: $0.14/kWh)
    """
    output_path = Path(output_path)
    report = generate_cost_report(df, rate_per_kwh)
    report_text = format_cost_report(report)

    output_path.write_text(report_text)
    logger.info(f"Cost report saved to {output_path}")
