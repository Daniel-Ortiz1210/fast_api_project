from .db import engine, Base
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer, DateTime

class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50)) 
    last_name = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(255))
    age = Column(Integer)
    curp = Column(String(18))
    rfc = Column(String(13))
    cp = Column(String(5))
    date = Column(DateTime())
    telephone = Column(String(10))
    user_type = Column(String(20))


def init_db(drop_all_tables=False):
    if drop_all_tables:
        try:
            print("Droping all tables...")
            Base.metadata.drop_all(bind=engine)
            print("SUCCESS")
        except:
            print("Error while droping tables")
    else:
        try:
            print("Creating all tables...")
            Base.metadata.create_all(bind=engine)
            print("SUCCESS")
        except:
            print("Error while creating tables")