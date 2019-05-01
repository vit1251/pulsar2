
from asyncio import get_event_loop

class Arbiter(object):
    """ Arbiter a very special actor which controls the life of all actors

    To use actors in pulsar you need to start the Arbiter, a very special actor which controls the life of all
    actors spawned during the execution of your code.

    """
    def __init__(self, loop=None):
        self.__log = getLogger('pulsar2.Arbiter')
        self._loop = loop or get_event_loop()

    def start(self):
        """ Start
        """
        self._loop.run_forever()

    def stop(self):
        """ Stop
        """
