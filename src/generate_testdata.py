# Script using SQLAlchemy expression language for creation of timescaledb tables and rows with random data
# deletes pre-existing tables
import sys

sys.path.insert(0, "/usr/src/script")  # append path

from sqlalchemy import inspect
from script.db import engine, MAX_DECIMAL_DIGITS
from decimal import getcontext
from script.db.utils import create_db, drop_db
import script.db.tables as tables
from datetime import datetime, timedelta
from random import random, choice, uniform
from schemas import ValueType, DataType
from collections import defaultdict


## CONSTANTS
getcontext().prec = (
    MAX_DECIMAL_DIGITS * 2 - 1
)  # Set precision for handing decimal values

## CUSTOMIZATION
num_days = 60  # number of days to generate data for
timestep_in_minutes = 10  # interval between sensor datapoints


## Sanity check
assert timestep_in_minutes > 1 & timestep_in_minutes < 60


print("Checking for existing tables...")
insp = inspect(engine)
if not insp.has_table("timeseries"):
    print("Tables not found, creating tables.\n")
    create_db(engine=engine)

else:
    print("Tables found... Dropping tables and recreating...")
    drop_db(engine=engine)
    create_db(engine=engine)

print("done creating tables...")
# create random type/ location info in sensors
timeseries_keys = [
    "type",
    "description",
    "name",
    "location",
    "unit",
    "value_type",
    "data_type",
]
timeseries_data = [
    (
        "device",
        "temperature",
        "primary core",
        "transformer 1",
        "Celcius",
        ValueType.DECIMAL,
        DataType.CONTINUOUS,
    ),
    (
        "device",
        "L1 voltage",
        "L1",
        "transformer 1",
        "Volt",
        ValueType.DECIMAL,
        DataType.CONTINUOUS,
    ),
    (
        "device",
        "L2 voltage",
        "L2",
        "transformer 1",
        "Volt",
        ValueType.DECIMAL,
        DataType.CONTINUOUS,
    ),
    (
        "device",
        "L3 voltage",
        "L3",
        "transformer 1",
        "Volt",
        ValueType.DECIMAL,
        DataType.CONTINUOUS,
    ),
    (
        "device",
        "operating mode",
        "transformer operating mode",
        "transformer 1",
        "state",
        ValueType.TEXT,
        DataType.DISCRETE,
    ),
]

with engine.connect() as db:
    print("creating timeseries...")
    db.execute(
        tables.timeseries.insert(),
        [dict(zip(timeseries_keys, a_ts_data)) for a_ts_data in timeseries_data],
    )

# create whole minute starting point for sensor data and create 31 days of random data for each device
now = datetime.now().timetuple()
now = datetime(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)

all_states = ["OP MODE 1", "OP MODE 2", "OFFLINE", "ISLAND MODE"]

print("inserting timeseries datapoints...")
inserts = defaultdict(list)
with engine.connect() as db:
    for time_offset in range(int(num_days * 24 * 60 / timestep_in_minutes)):
        dt = now - timedelta(minutes=time_offset * timestep_in_minutes)
        for sensor in range(len(timeseries_data)):
            if sensor < len(timeseries_data) - 1:
                # continuous
                table = tables.datapoint_numeric
                if sensor == 0:
                    value = 100 * random()
                else:
                    value = 220 + uniform(-5, 5)
            else:
                table = tables.datapoint_str
                value = (
                    choice(all_states) if time_offset % 24 == 0 else None
                )  # reduce number of state events
            if value:
                inserts[table].append({"ts": dt, "ts_id": sensor + 1, "value": value})

    for table, entries in inserts.items():
        db.execute(table.insert(), entries)
print("completed generating testdata...")
