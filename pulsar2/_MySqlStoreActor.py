
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

    def _restore(self, key=None):
        """ Restore `value` under `key` name from MySQL
        """
        return None
