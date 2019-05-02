
from logging import getLogger
from aiohttp import ClientSession

from ._Actor import Actor

class HttpClientActor(Actor):
    def __init__(self, *args, **kwargs):
        Actor.__init__(self, *args, **kwargs)
        #
        self.__log = getLogger('pulsar2.HttpClientActor')
        self._commands['fetch'] = self._fetch

    async def _fetch(self, url, receiver=None):
        """ Fetch
        """
        self.__log.debug('fetch: url = {url!r}'.format(url=url))
        #
        async with ClientSession() as session:
            async with session.get(url) as response:
                value = await response.text()
                if receiver:
                    aid, action = receiver
                else:
                    self.__log.warn('No receiver.')
