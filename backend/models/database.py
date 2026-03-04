import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv


load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

engine = db.create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", echo=True)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session=session()

Base = declarative_base()  #every class will inherit from Base to declare class -> table & attribute -> column

# try:
#     with engine.connect() as conn:
#         print("Connection successful!")
# except Exception as e:
#     print("Connection failed:", e)       #To check that I connect successfully to the database or not
#
