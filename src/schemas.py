from decimal import Decimal
from script.db.tables import MAX_DECIMAL_DIGITS, STR_MAXLEN
from dataclasses import dataclass

######### CONSTANT DEFINITIONS
MAX_DECIMAL = Decimal(10) ** -MAX_DECIMAL_DIGITS


@dataclass
# Core helper function that enables IntEnum type functionality in/out DB where DB uses int values and json/Pydantic schemas use str
class ValueType:
    TEXT: int = 1
    INT: int = 2
    DECIMAL: int = 3


@dataclass
class DataType:
    CONTINUOUS: int = 1  # typical sensor / device data
    DISCRETE: int = 2  # discrete or categorical data
