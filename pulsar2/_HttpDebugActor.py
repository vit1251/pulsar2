
from logging import getLogger
from aiohttp import web

from ._Actor import Actor

class HttpDebugActor(Actor):
    def __init__(self, arbiter, *args, **kwargs):
        Actor.__init__(self, arbiter, *args, **kwargs)
        self.__log = getLogger('pulsar2.HttpDebugAgent')
        self._runner = None

    async def handle(self, request):
        """
        """
        resp = []
        for aid, agent in self._arbiter._managed_actors.items():
            item = {
                'name': '',
                'aid': aid,
                'info': agent.info(),
            }
            resp.append(item)
        return web.json_response(resp)

    async def _start(self):
        """ Start Web-server
        """
        app = web.Application()
        app.add_routes([
            web.get('/', self.handle),
        ])
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, '0.0.0.0', 9999)
        await site.start()

    async def _stop(self):
        """ Stop Web-server
        """
        await self._runner.cleanup()

    async def run(self):
#        self._loop.create_task()
        self.__log.debug("Start")
        await self._start()
