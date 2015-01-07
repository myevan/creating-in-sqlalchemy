from db_shard_proto import DBShardProto
from db_shard_manager import DBShardManager
from db_manager import DBManager

GLOBAL_MASTER_DB_URI = 'sqlite:///temp/global_m.sq3'
GLOBAL_SLAVE_DB_URI = 'sqlite:///temp/global_m.sq3'

USER_MASTER_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///temp/user_m_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///temp/user_m_shard_2.sq3')
]

LOG_MASTER_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///temp/log_m_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///temp/log_m_shard_2.sq3')
]

USER_SLAVE_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///temp/user_s_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///temp/user_s_shard_2.sq3')
]

LOG_SLAVE_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///temp/log_s_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///temp/log_s_shard_2.sq3')
]

if __name__ == '__main__':
    import os
    import log_db
    import user_db
    import global_db

    if not os.access('temp', os.R_OK):
        os.makedirs('temp')

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
