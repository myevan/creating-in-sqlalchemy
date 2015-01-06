from sqlalchemy import create_engine
from contextlib import closing

test_db_engine = create_engine('sqlite:///:memory:', echo=True)

if __name__ == '__main__':
    with closing(test_db_engine.connect()) as conn:
        pass