from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
MasterSession = sessionmaker()
SlaveSession = sessionmaker()
