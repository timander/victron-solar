"""Pydantic models for solar CSV ingestion and validation."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SolarRecord(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the measurement")
    voltage: float = Field(..., description="Voltage in volts")
    current: float = Field(..., description="Current in amperes")
    power: float = Field(..., description="Power in watts")
    energy: Optional[float] = Field(None, description="Cumulative energy in watt-hours")

    class Config:
        extra = "forbid"
        anystr_strip_whitespace = True
