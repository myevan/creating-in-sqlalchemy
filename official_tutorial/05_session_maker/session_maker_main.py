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

