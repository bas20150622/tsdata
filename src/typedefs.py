# Script defining custom typing models
from typing import Union, Optional
from script.db import tables
import schemas as schemas
from sqlalchemy.engine import Row
from sqlalchemy import Table


DBTables = Table  # models can be used in typing union but not tables
"""Union[
    tables.datapoint_int,
    tables.datapoint_numeric,
    tables.datapoint_str,
    tables.timeseries,
]"""

DataDBTables = Table
"""Union[
    tables.datapoint_int, tables.datapoint_numeric, tables.datapoint_str
]"""

DataSchemaModels = Union[schemas.DatapointCreate, schemas.TimeseriesCreate]

SchemaModels = Union[
    schemas.DatapointCreate,
    schemas.TimeseriesCreate,
]

RowOrNone = Optional[Row]
