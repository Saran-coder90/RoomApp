# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


# Define the database URL (SQLite for this example)
DATABASE_URL = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

print(DATABASE_URL)

# Create the database engine
engine = None
try:
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800)
    print("All are successfull")
except Exception as e:
    print("Failed!!! " + f'{e}')

     

# Create a sessionmaker to manage sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for models to inherit from
Base = declarative_base()

