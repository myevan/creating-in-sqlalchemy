from sqlalchemy import create_engine


class DBManager(object):
    def __init__(self, uri, session_cls, base_cls):
        self.uri = uri
        self.session_cls = session_cls
        self.base_cls = base_cls
        self.engine = None

    def connect_database(self, echo=False):
        self.engine = create_engine(self.uri, echo=echo)

        self.session_cls.configure(bind=self.engine)

    def drop_all_tables(self):
        self.base_cls.metadata.drop_all(self.engine)

    def create_all_tables(self, checkfirst=True):
        self.base_cls.metadata.create_all(
            self.engine, checkfirst=checkfirst)
