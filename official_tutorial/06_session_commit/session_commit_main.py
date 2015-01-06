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

    old_user = test_db_session.query(User).filter_by(name='user1').first()
    assert(old_user is new_user)

    test_db_session.add_all([
        User(name='user2', password='5678'),
        User(name='user3', password='abcd'),
        ])

    old_user.password = 'xyzw'
    print('dirty_set:{0}'.format(test_db_session.dirty))
    print('new_set:{0}'.format(test_db_session.new))

    test_db_session.commit()

    print('old_user_id:{0}'.format(old_user.id))

