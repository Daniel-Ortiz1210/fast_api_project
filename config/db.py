from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import scoped_session, sessionmaker

USER = "root"
PASSWORD = "Dex122706"
DB = "users"

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3306/{DB}")
sessionmaker = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = scoped_session(sessionmaker)
Base = declarative_base()