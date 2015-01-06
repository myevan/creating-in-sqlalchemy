from sqlalchemy import create_engine
from contextlib import closing

if __name__ == '__main__':
    test_db_engine = create_engine('sqlite:///:memory:', echo=True)

    with closing(test_db_engine.connect()) as conn:
        pass