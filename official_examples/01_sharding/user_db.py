from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from random import randrange

from guoid import GUOIDGenerator

Base = declarative_base()
MasterSession = scoped_session(sessionmaker(class_=ShardedSession))
SlaveSession = scoped_session(sessionmaker(class_=ShardedSession))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    money = Column(Integer)

    items = relationship(lambda: Item, backref='owner')

    def __repr__(self):
        return '<User(id={0}, name={1}, money={2})>'.format(
            self.id, self.name, self.money)

    @classmethod
    def create_user_with_device(cls, device, *args, **kwargs):
        new_user = cls(*args, **kwargs)
        new_user.id = (device.id << 8) | randrange(0, 255)
        return new_user

    @property
    def logical_shard_id(self):
        return self.id & 0xff


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    proto_id = Column(Integer)

    user_id = Column(Integer, ForeignKey(User.id))

    @classmethod
    def create_item_with_owner(cls, owner, *args, **kwargs):
        new_item = cls(*args, **kwargs)
        new_item.owner = owner
        new_item.id = GUOIDGenerator.instance.gen_guoid(owner.logical_shard_id)
        return new_item

