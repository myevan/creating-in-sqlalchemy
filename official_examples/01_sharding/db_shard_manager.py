from sqlalchemy import create_engine
from sqlalchemy.sql import operators, visitors


class DBShardManager(object):
    def __init__(self, shard_protos, session_cls, base_cls, main_cls=None, primary_key_name=None, foreign_key_name=None):
        self.session_cls = session_cls
        self.shard_protos = shard_protos
        self.shard_engines = []
        self.shard_dict = {}

        self.base_cls = base_cls
        self.main_cls = main_cls
        self.primary_key_name = primary_key_name
        self.foreign_key_name = foreign_key_name

        self.primary_key_column = getattr(main_cls, primary_key_name) if main_cls and primary_key_name else None

    def connect_database(self, echo=False):
        for shard_proto in self.shard_protos:
            shard_engine = create_engine(shard_proto.uri, echo=echo)
            self.shard_engines.append(shard_engine)
            self.shard_dict[shard_proto.key] = shard_engine

        self.session_cls.configure(
            shards=self.shard_dict,
            shard_chooser=self._choose_shard,
            query_chooser=self._choose_query,
            id_chooser=self._choose_id)

    def _choose_id(self, query, instance_ids):
        print('choose_ids:{0} query:{1}'.format(instance_ids, query))

        shard_keys = set()
        for instance_id in instance_ids:
            shard_keys.add(self._convert_shard_key(instance_id))

        return shard_keys

    def _choose_shard(self, mapper, instance, clause=None):
        print('choose_shard:{0}'.format(instance))
        if isinstance(instance, self.main_cls):
            key_value = getattr(instance, self.primary_key_name)
            if key_value is None:
                raise ValueError('NOT_SUPPORTED_INSTANCE:{0}'.format(instance))
        else:
            key_value = getattr(instance, self.foreign_key_name)
            if key_value is None:
                raise ValueError('NOT_SUPPORTED_INSTANCE:{0}'.format(instance))

        return self._convert_shard_key(key_value)

    def _choose_query(self, query):
        print('choose_query:{0}'.format(query))
        shard_keys = set()
        for column, operator, value in self._get_query_comparisons(query):
            is_foregin_column = False
            for foreign_key in column.foreign_keys:
                if foreign_key._colspec is self.primary_key_column:
                    is_foregin_column = True

            is_lineage_column = column.shares_lineage(self.primary_key_column)
            if is_foregin_column or is_lineage_column:
                if operator == operators.eq:
                    shard_keys.add(
                        self._convert_shard_key(value))
                elif operator == operators.in_op:
                    shard_keys.update(
                        self._convert_shard_key(item) for item in value)

        if len(shard_keys):
            return shard_keys
        else:
            return self.shard_dict.keys()

    @staticmethod
    def _get_query_comparisons(query):
        binds = {}
        clauses = set()
        comparisons = []

        def visit_bindparam(bind):
            if bind.key in query._params:
                value = query._params[bind.key]
            elif bind.callable:
                value = bind.callable()
            else:
                value = bind.value

            binds[bind] = value

        def visit_column(column):
            clauses.add(column)

        def visit_binary(binary):
            if binary.left in clauses and \
                    binary.operator == operators.in_op and \
                    hasattr(binary.right, 'clauses'):
                comparisons.append(
                    (binary.left, binary.operator,
                        tuple(binds[bind] for bind in binary.right.clauses)
                    )
                )
            elif binary.left in clauses and binary.right in binds:
                comparisons.append(
                    (binary.left, binary.operator,binds[binary.right])
                )

            elif binary.left in binds and binary.right in clauses:
                comparisons.append(
                    (binary.right, binary.operator,binds[binary.left])
                )

        if query._criterion is not None:
            visitors.traverse_depthfirst(
                query._criterion,
                {},
                {
                    'bindparam': visit_bindparam,
                    'binary': visit_binary,
                    'column': visit_column
                }
            )
        return comparisons

    def _convert_shard_key(self, value):
        logical_shard_id = (value & 0xff)
        physical_shard_id = logical_shard_id / 128 # TODO: Customizing
        return physical_shard_id

    def drop_all_tables(self):
        for shard_engine in self.shard_engines:
            self.base_cls.metadata.drop_all(shard_engine)

    def create_all_tables(self, checkfirst=True):
        for shard_engine in self.shard_engines:
            self.base_cls.metadata.create_all(
                shard_engine, checkfirst=checkfirst)
