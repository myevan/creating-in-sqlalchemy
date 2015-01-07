from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
MasterSession = sessionmaker()
SlaveSession = sessionmaker()


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(String(32), nullable=False)

    def __repr__(self):
        return '<Device(id={0}, guid={1}, logical_shard_id={2})>'.format(
            self.id, self.guid, self.logical_shard_id)

    @classmethod
    def create_device(cls, *args, **kwargs):
        return cls(*args, **kwargs)


