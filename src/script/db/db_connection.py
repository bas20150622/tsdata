"""
Script containing db connection methods
"""
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()


connection_info = {
    "drivername": os.getenv("POSTGRES_DRIVER"),
    "database": os.getenv("POSTGRES_DB"),
    "username": os.getenv("POSTGRES_USER"),
    "port": os.getenv("POSTGRES_PORT"),
    "host": os.getenv("POSTGRES_HOST"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}
# connection_info["host"] = "localhost"

connect_args = (
    {"sslmode": "require"} if "azure.com" in connection_info.get("host") else {}
)

_DB_URL = URL.create(**connection_info)
engine = create_engine(_DB_URL, connect_args=connect_args, echo=False)
