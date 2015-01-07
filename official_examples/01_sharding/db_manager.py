from sqlalchemy import create_engine


class DBManager(object):
    def __init__(self, base_cls, session_cls, uri, echo=False):
        self.base_cls = base_cls
        self.session_cls = session_cls
        self.uri = uri
        self.engine = None
        self.echo = echo

    def connect_database(self):
        self.engine = create_engine(self.uri, echo=self.echo)

    def drop_all_tables(self):
        self.base_cls.metadata.drop_all(self.engine)

    def create_all_tables(self, checkfirst=True):
        self.base_cls.metadata.create_all(
            self.engine, checkfirst=checkfirst)
