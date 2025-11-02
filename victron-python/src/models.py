"""Pydantic models for solar CSV ingestion and validation."""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class SolarRecord(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the measurement")
    voltage: float = Field(..., description="Voltage in volts")
    current: float = Field(..., description="Current in amperes")
    power: float = Field(..., description="Power in watts")
    energy: Optional[float] = Field(None, description="Cumulative energy in watt-hours")

    model_config = ConfigDict({
        "extra": "forbid",
        "str_strip_whitespace": True
    })
