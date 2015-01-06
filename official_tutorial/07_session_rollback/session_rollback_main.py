from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    password = Column(String)

    def __repr__(self):
        return '<User(id={0}, name={1}, password={2})>'.format(
            self.id, self.name, self.password)


if __name__ == '__main__':
    test_db_engine = create_engine('sqlite:///:memory:', echo=True)

    Base.metadata.create_all(test_db_engine)

    TestDBSession = sessionmaker(bind=test_db_engine)

    test_db_session = TestDBSession()

    new_user = User(name='user1', password='1234')
    test_db_session.add(new_user)
    print('new_user_added:{0}'.format(new_user))
    test_db_session.commit()

    old_user = test_db_session.query(User).filter_by(name='user1').first()
    old_user.name = 'USER1'
    print('old_user_changed:{0}'.format(old_user))

    fake_user = User(name='userX', password='XXXX')
    test_db_session.add(fake_user)
    print('fake_user_added:{0}'.format(test_db_session.query(User).filter_by(name='userX').first()))

    test_db_session.rollback()

    print('old_user_rollbacked:{0}'.format(old_user))
    print('fake_user_rollbacked:{0}'.format(test_db_session.query(User).filter_by(name='userX').first()))
