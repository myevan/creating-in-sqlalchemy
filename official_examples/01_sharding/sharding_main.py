from db_shard_proto import DBShardProto
from db_shard_manager import DBShardManager
from db_manager import DBManager

GLOBAL_MASTER_DB_URI = 'sqlite:///temp/global_m.sq3'

USER_MASTER_DB_SHARD_PROTOS = [
    DBShardProto(key=0, uri='sqlite:///temp/user_m_shard_1.sq3'),
    DBShardProto(key=1, uri='sqlite:///temp/user_m_shard_2.sq3')
]


def init_db_managers(db_managers):
    for db_manager in db_managers:
        db_manager.connect_database(echo=True)
        db_manager.drop_all_tables()
        db_manager.create_all_tables()


def make_user(device_guid):
    gdm_session = global_db.MasterSession()
    new_device = global_db.Device(guid=device_guid)
    gdm_session.add(new_device)
    gdm_session.commit()

    udm_session = user_db.MasterSession()
    new_user = user_db.User(money=100, device=new_device)
    new_item = user_db.Item(proto_id=1, owner=new_user)
    udm_session.add(new_user)
    udm_session.add(new_item)
    udm_session.flush()

    new_user_id = new_user.id
    udm_session.commit()
    return new_user_id


if __name__ == '__main__':
    import os
    import user_db
    import global_db

    if not os.access('temp', os.R_OK):
        os.makedirs('temp')

    db_managers = [
        DBManager(
            GLOBAL_MASTER_DB_URI,
            global_db.MasterSession,
            global_db.Base),
        DBShardManager(
            USER_MASTER_DB_SHARD_PROTOS,
            user_db.MasterSession,
            user_db.Base,
            user_db.User,
            'id',
            'user_id'),
    ]

    init_db_managers(db_managers)
    a_user_id = make_user('aaaa')
    b_user_id = make_user('bbbb')
    c_user_id = make_user('bbbb')

    udm_session = user_db.MasterSession()
    test_user = udm_session.query(user_db.User).get(a_user_id)
    test_item = test_user.items[0]
    test_item_id = test_item.id

    print '!!!!!!!!!!!!!'
    test_item2 = udm_session.query(user_db.Item).get(test_item_id)

    if 0:
        for each_user in udm_session.query(user_db.User).filter_by(money=1000):
            print each_user
