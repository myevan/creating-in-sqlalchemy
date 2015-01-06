from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return '<User(id={0}, name={1})>'.format(self.id, self.name)



if __name__ == '__main__':
    test_db_engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(test_db_engine)

