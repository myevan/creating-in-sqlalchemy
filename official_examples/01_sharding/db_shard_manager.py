from sqlalchemy import create_engine


class DBShardManager(object):
    def __init__(self, base_cls, session_cls, shard_protos):
        self.base_cls = base_cls
        self.session_cls = session_cls
        self.shard_protos = shard_protos
        self.shard_engines = []
        self.shard_dict = {}

    def connect_database(self, echo=True):
        for shard_proto in self.shard_protos:
            shard_engine = create_engine(shard_proto.uri, echo=echo)
            self.shard_engines.append(shard_engine)
            self.shard_dict[shard_proto.key] = shard_engine

        self.session_cls.configure(shards=self.shard_dict)

    def drop_all_tables(self):
        for shard_engine in self.shard_engines:
            self.base_cls.metadata.drop_all(shard_engine)

    def create_all_tables(self, checkfirst=True):
        for shard_engine in self.shard_engines:
            self.base_cls.metadata.create_all(
                shard_engine, checkfirst=checkfirst)
