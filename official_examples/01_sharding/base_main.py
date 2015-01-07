from framework.db_manager import DBManager
from framework.db_shard_manager import DBShardManager
from framework.db_shard_proto import DBShardProto

GLOBAL_MASTER_DB_URI = 'sqlite:///global_m.sq3'
GLOBAL_SLAVE_DB_URI = 'sqlite:///global_m.sq3'

USER_MASTER_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///user_m_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///user_m_shard_2.sq3')
]

LOG_MASTER_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///log_m_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///log_m_shard_2.sq3')
]

USER_SLAVE_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///user_s_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///user_s_shard_2.sq3')
]

LOG_SLAVE_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///log_s_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///log_s_shard_2.sq3')
]

if __name__ == '__main__':
    import log_db
    import user_db
    import global_db

    db_managers = [
        DBManager(
            global_db.Base, global_db.MasterSession, GLOBAL_MASTER_DB_URI),
        DBManager(
            global_db.Base, global_db.SlaveSession, GLOBAL_SLAVE_DB_URI),
        DBShardManager(
            user_db.Base, user_db.MasterSession, USER_MASTER_DB_SHARD_PROTOS),
        DBShardManager(
            user_db.Base, user_db.SlaveSession, USER_SLAVE_DB_SHARD_PROTOS),
        DBShardManager(
            log_db.Base, log_db.MasterSession, LOG_MASTER_DB_SHARD_PROTOS),
        DBShardManager(
            log_db.Base, log_db.SlaveSession, LOG_SLAVE_DB_SHARD_PROTOS),
    ]

    for db_manager in db_managers:
        db_manager.connect_database()
        db_manager.drop_all_tables()
        db_manager.create_all_tables()
