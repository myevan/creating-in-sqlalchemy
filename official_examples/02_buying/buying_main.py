from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    money = Column(Integer)

    def __repr__(self):
        return '<User(id={0}, name={1}, password={2})>'.format(
            self.id, self.name, self.password)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    proto_id = Column(Integer)


if __name__ == '__main__':
    import argparse
    import sys
    import time

    from multiprocessing.pool import ThreadPool

    arg_parser = argparse.ArgumentParser(description='test buying')
    arg_parser.add_argument('-U', '--uri', type=str, help='Database URI schema://username:password@db_host/db_name')
    arg_parser.add_argument('-R', '--reset', action='store_true', help='Reset Database')
    args = arg_parser.parse_args()

    if not args.uri:
        print('no_uri')
        sys.exit(-1)

    test_engine = create_engine(args.uri, echo=True)

    TestSession = scoped_session(sessionmaker(bind=test_engine))

    if args.reset:
        Base.metadata.drop_all(test_engine)
        Base.metadata.create_all(test_engine)

        test_session = TestSession()
        test_session.add(User(name='user1', money=10000))
        test_session.add(User(name='user2', money=10000))
        test_session.commit()

    def buy(name):
        test_session = TestSession()
        buyer = test_session.query(User).filter_by(name=name).with_for_update().one()

        before_money = buyer.money
        if buyer.money < 100:
            return 'error', name, before_money, before_money, None

        buyer.money -= 100

        new_item = Item(proto_id=1, user_id=buyer.id)
        test_session.add(new_item)
        test_session.flush()

        taken_item_id = new_item.id
        after_money = buyer.money

        test_session.commit()

        return 'ok', name, before_money, after_money, taken_item_id

    pool = ThreadPool(6)
    for status, name, before_money, after_money, item_id in pool.map(buy, ['user1'] * 2 + ['user2'] * 2 + ['user1'] * 2):
        print status, name, before_money, after_money, item_id
