#!/usr/bin/env python

from sqlalchemy import create_engine
from archiver.models import Base
import os

DB = os.getenv("POSTGRES_DB", "library")
HOST = os.getenv("POSTGRES_HOST", "library")
PORT = os.getenv("POSTGRES_PORT", "5432")
USER = os.getenv("POSTGRES_USER", "librarian")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "<yourpassword>")

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

def init_db():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema created.")

if __name__ == "__main__":
    init_db()
