from .db import engine, Base
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer, DateTime

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50)) 
    last_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(255))
    age = Column(Integer)
    curp = Column(String(18))
    rfc = Column(String(13))
    cp = Column(String(5))
    date = Column(DateTime())
    telephone = Column(String(10))
    user_type = Column(String(20))


def init_db(initialize=True):
    if initialize:
        Base.metadata.create_all(bind=engine)
    else:
        Base.metadata.drop_all(bind=engine)
