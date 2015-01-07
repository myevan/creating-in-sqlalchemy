import time


class GUOIDGenerator(object):
    """
    https://github.com/charsyam/python-guoid
    """
    LOGICAL_SHARD_BITS = 8
    LOGICAL_SHARD_MASK = (1 << LOGICAL_SHARD_BITS) - 1

    SEQUENCE_BITS = 12
    SEQUENCE_MASK = (1 << SEQUENCE_BITS) - 1

    SEQUENCE_SHIFT = LOGICAL_SHARD_BITS
    TIMESTAMP_SHIFT = LOGICAL_SHARD_BITS + SEQUENCE_BITS

    instance = None

    @classmethod
    def create_instance(cls, base_timestamp):
        cls.instance = cls(base_timestamp)

    def __init__(self, base_timestamp):
        self.base_timestamp = base_timestamp
        self.last_timestamp = 0
        self.sequence = 0

    def gen_guoid(self, logical_shard_id):
        cur_timestamp = self._get_timestamp()
        if cur_timestamp < self.last_timestamp:
            raise RuntimeError("CLOCK_MOVED_BACKWARDS")

        if cur_timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.SEQUENCE_MASK
            if self.sequence == 0:
                cur_timestamp = self.wait_for_next_timestamp(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = cur_timestamp
        rel_timestamp = cur_timestamp - self.base_timestamp

        ret_guoid = (rel_timestamp << self.TIMESTAMP_SHIFT)
        ret_guoid |= (self.sequence << self.SEQUENCE_SHIFT)
        ret_guoid |= logical_shard_id
        print self.sequence
        return ret_guoid

    @staticmethod
    def _get_timestamp():
        return int((time.time()) * 1000)

    @classmethod
    def _wait_for_next_timestamp(cls, last_timestamp):
        cur_timestamp = cls._get_timestamp()
        while cur_timestamp <= last_timestamp:
            cur_timestamp = cls.get_timestamp()

        return cur_timestamp

if __name__ == '__main__':
    guoidGenerator = GUOIDGenerator(1420623826669)
    print '%x' % guoidGenerator.gen_guoid(0)
    time.sleep(1)
    print '%x' % guoidGenerator.gen_guoid(0)
