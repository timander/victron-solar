"""Initial test for SolarPipeline (TDD setup)."""

import os

from src.pipeline import SolarPipeline


def test_pipeline_instantiation():
    csv_path = os.environ.get("CSV", "../data/SolarHistory.csv")
    pipeline = SolarPipeline(csv_path)
    assert isinstance(pipeline, SolarPipeline)


# TODO: Update these tests to use the new SolarRecord model with actual CSV schema
# def test_solar_record_valid():
#     from src.models import SolarRecord
#
#     record = SolarRecord(
#         timestamp="2025-11-02T12:00:00", voltage=48.5, current=10.2, power=494.7, energy=12345.6
#     )
#     assert record.voltage == 48.5
#     assert record.energy == 12345.6
#
#
# def test_solar_record_invalid():
#     from src.models import SolarRecord
#
#     with pytest.raises(Exception):
#         SolarRecord(
#             timestamp="not-a-date",
#             voltage="bad",
#             current=None,
#             power=100,
#         )
