from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, Session

engine = create_engine("mysql+pymysql://root:Dex122706@localhost:3306/users")
Base = declarative_base()
session = Session(engine)