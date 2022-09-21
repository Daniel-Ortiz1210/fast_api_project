from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("mysql+pymysql://root:Dex122706@localhost:3306/users")
sessionmaker = sessionmaker(bind=engine,autocommit=False, autoflush=False)
session = scoped_session(sessionmaker)
Base = declarative_base()