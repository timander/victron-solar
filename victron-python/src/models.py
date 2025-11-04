"""Pydantic models for solar CSV ingestion and validation."""


from pydantic import BaseModel, ConfigDict, Field, field_validator


class SolarRecord(BaseModel):
    """Model representing a single day's solar panel data from Victron equipment."""

    days_ago: int = Field(..., alias="Days ago", description="Number of days ago from today")
    date: str = Field(..., alias="Date", description="Date in MM/DD/YY format")
    yield_wh: float = Field(
        ..., alias="Yield(Wh)", ge=0, description="Daily solar yield in watt-hours"
    )
    consumption_wh: float = Field(
        ..., alias="Consumption(Wh)", ge=0, description="Daily consumption in watt-hours"
    )
    max_pv_power_w: float = Field(
        ..., alias="Max. PV power(W)", ge=0, description="Maximum PV power in watts"
    )
    max_pv_voltage_v: float = Field(
        ..., alias="Max. PV voltage(V)", ge=0, description="Maximum PV voltage in volts"
    )
    min_battery_voltage_v: float = Field(
        ..., alias="Min. battery voltage(V)", ge=0, description="Minimum battery voltage in volts"
    )
    max_battery_voltage_v: float = Field(
        ..., alias="Max. battery voltage(V)", ge=0, description="Maximum battery voltage in volts"
    )
    time_in_bulk_m: int = Field(
        ..., alias="Time in bulk(m)", ge=0, description="Time in bulk charge phase in minutes"
    )
    time_in_absorption_m: int = Field(
        ..., alias="Time in absorption(m)", ge=0, description="Time in absorption phase in minutes"
    )
    time_in_float_m: int = Field(
        ..., alias="Time in float(m)", ge=0, description="Time in float phase in minutes"
    )
    last_error: int = Field(..., alias="Last error", description="Last error code")
    second_last_error: int = Field(
        ..., alias="2nd last error", description="Second last error code"
    )
    third_last_error: int = Field(..., alias="3rd last error", description="Third last error code")
    fourth_last_error: int = Field(
        ..., alias="4th last error", description="Fourth last error code"
    )

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        populate_by_name=True,  # Allow using both field name and alias
    )

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date is in MM/DD/YY format."""
        parts = v.split("/")
        if len(parts) != 3:
            raise ValueError(f"Date must be in MM/DD/YY format, got: {v}")
        return v


class SolarSummary(BaseModel):
    """Model for pipeline summary statistics."""

    total_yield_wh: float = Field(..., description="Total solar yield in watt-hours")
    max_pv_power_w: float = Field(..., description="Maximum PV power in watts")
    max_pv_voltage_v: float = Field(..., description="Maximum PV voltage in volts")
    min_battery_voltage_v: float = Field(..., description="Minimum battery voltage in volts")
    max_battery_voltage_v: float = Field(..., description="Maximum battery voltage in volts")
    total_days: int = Field(..., description="Total number of days in dataset")

    model_config = ConfigDict(
        extra="forbid",
    )
