
from aiohttp import ClientSession

from ._Actor import Actor

class HttpClientActor(Actor):
    def __init__(self, *args, **kwargs):
        Actor.__init__(self, *args, **kwargs)
        #
        self._commands['fetch'] = self._fetch

    async def _fetch(self, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
