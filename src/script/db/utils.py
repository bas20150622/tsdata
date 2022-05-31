"""
DB utility functions
"""

from sqlalchemy.sql import text
from sqlalchemy.engine import Engine
from script.db.tables import (
    timeseries,
    datapoint_int,
    datapoint_numeric,
    datapoint_str,
    metadata_obj,
)
from script.db import engine

_tables = [timeseries, datapoint_int, datapoint_numeric, datapoint_str]


def drop_db(engine: Engine):
    """Drop tables - automatically removes TimescaleDB hypertables"""
    metadata_obj.drop_all(engine, tables=_tables, checkfirst=True)


def create_db(engine: Engine):
    """Create tables and TimescaleDB hypertables"""
    metadata_obj.create_all(engine, tables=_tables, checkfirst=True)

    with engine.connect() as conn:

        stmt = text("SELECT create_hypertable(:table, :field);").bindparams(
            table="datapoint_int", field="ts"
        )
        result = conn.execute(stmt)  # create timescaleDB hypertable

        stmt = text("SELECT create_hypertable(:table, :field);").bindparams(
            table="datapoint_str", field="ts"
        )
        result = conn.execute(stmt)  # create timescaleDB hypertable

        stmt = text("SELECT create_hypertable(:table, :field);").bindparams(
            table="datapoint_numeric", field="ts"
        )
        result = conn.execute(stmt)  # create timescaleDB hypertable
