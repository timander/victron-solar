"""Initial test for SolarPipeline (TDD setup)."""
import pytest
from victron.pipeline import SolarPipeline

def test_pipeline_instantiation():
    pipeline = SolarPipeline()
    assert isinstance(pipeline, SolarPipeline)
