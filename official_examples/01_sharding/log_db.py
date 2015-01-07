from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.horizontal_shard import ShardedSession

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
MasterSession = sessionmaker(class_=ShardedSession)
SlaveSession = sessionmaker(class_=ShardedSession)
