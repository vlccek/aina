import datetime
from sqlalchemy import Boolean, Column, String, Integer, DateTime


# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"

DATABASE_URI = "postgres://postgres:root@db_aina:5432/aina"
