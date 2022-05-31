# .env

# For the Postgres/TimescaleDB database. 
PGDATA=/var/lib/postgresql/data
POSTGRES_USER=demo
POSTGRES_PASSWORD=nopassword
POSTGRES_HOST=timescale
POSTGRES_PORT=5432
POSTGRES_DB=transformer
POSTGRES_DRIVER=postgresql+psycopg2


# For the PGAdmin web app
PGADMIN_DEFAULT_EMAIL=not.valid@email.com
PGADMIN_DEFAULT_PASSWORD=no_password
PGADMIN_LISTEN_PORT=9000

PYTHONUNBUFFERED=1 # print statements are visible in docker
PYTHONDONTWRITEBYTECODE=1