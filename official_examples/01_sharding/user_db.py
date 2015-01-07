from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from random import randrange

Base = declarative_base()
MasterSession = scoped_session(sessionmaker(class_=ShardedSession))
SlaveSession = scoped_session(sessionmaker(class_=ShardedSession))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    money = Column(Integer)

    items = relationship(lambda: Item, backref='owner')

    def __init__(self, device, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        self.id = (device.id << 8) | randrange(0, 255)

    def __repr__(self):
        return '<User(id={0}, name={1}, money={2})>'.format(
            self.id, self.name, self.money)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    proto_id = Column(Integer)

    user_id = Column(Integer, ForeignKey(User.id))

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)

        self.id = (device.id << 8) | randrange(0, 255)

