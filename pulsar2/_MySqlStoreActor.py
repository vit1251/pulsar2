
from logging import getLogger
from ._Actor import Actor

class MySqlStoreActor(Actor):
    def __init__(self, *args, **kwargs):
        Actor.__init__(self, *args, **kwargs)
        self.__log = getLogger('pulsar2.MySqlStoreActor')
        #
        self._commands['store'] = self._store
        self._commands['restore'] = self._restore

    def _store(self, key=None, value=None):
        """ Store `value` under `key` name to MySQL
        """
        return None

    def _restore(self, key=None, receiver=None):
        """ Restore `value` under `key` name from MySQL
        """
        # Step 1. Receive value
        data = 'Test' # TODO - replace on real MySQL request ...

        # Step 1. Delivery result
        if receiver:
            aid, action = receiver
            self.send(aid, action, data=data)
        else:
            self.__log.warn('No result receiver.')
