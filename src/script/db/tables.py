"""
module for sqlalchemy tables
"""

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    DateTime,
    Numeric,
    Index,
)

# DEFINE NUMERIC CONSTRAINTS
MAX_DECIMAL_DIGITS = 8
SCALE = 4

STR_MAXLEN = 150

metadata_obj = MetaData()

timeseries = Table(
    "timeseries",
    metadata_obj,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("type", String(STR_MAXLEN)),
    Column("description", String(STR_MAXLEN), nullable=True),
    Column("location", String(STR_MAXLEN), nullable=True),
    Column("name", String(STR_MAXLEN), nullable=True),  # e.g. identifier
    Column(
        "unit", String(STR_MAXLEN), nullable=True
    ),  # description of the device measurement unit, i.e. Celcius or State
    Column(
        "value_type", Integer, nullable=False
    ),  # link to datapoint value type implementation
    Column(
        "data_type", Integer, nullable=False
    ),  # continuous vs discrete or categorical timeseries
)

datapoint_int = Table(
    "datapoint_int",
    metadata_obj,
    Column("ts", DateTime(timezone=True), nullable=False),
    Column("ts_id", Integer, ForeignKey("timeseries.id", ondelete="CASCADE")),
    Column("value", Integer),
)
Index("datapoint_int_time_ts_id_idx", datapoint_int.c.ts_id, datapoint_int.c.ts.desc())

datapoint_str = Table(
    "datapoint_str",
    metadata_obj,
    Column("ts", DateTime(timezone=True), nullable=False),
    Column("ts_id", Integer, ForeignKey("timeseries.id", ondelete="CASCADE")),
    Column("value", String(STR_MAXLEN)),
)
Index("datapoint_str_time_ts_id_idx", datapoint_str.c.ts_id, datapoint_str.c.ts.desc())

datapoint_numeric = Table(
    "datapoint_numeric",
    metadata_obj,
    Column("ts", DateTime(timezone=True), nullable=False),
    Column("ts_id", Integer, ForeignKey("timeseries.id", ondelete="CASCADE")),
    Column(
        "value", Numeric(precision=2 * MAX_DECIMAL_DIGITS, scale=MAX_DECIMAL_DIGITS)
    ),
)
Index(
    "datapoint_numeric_time_ts_id_idx",
    datapoint_numeric.c.ts_id,
    datapoint_numeric.c.ts.desc(),
)
