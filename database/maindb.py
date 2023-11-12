from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME_")
PASSWORD = os.getenv("PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
HOSTNAME = os.getenv("HOSTNAME")
engine = create_engine(f"mysql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}", echo=True)
Session = sessionmaker(engine)
session = Session()
Base = declarative_base()
