
from logging import getLogger
from aiohttp import web

from ._Actor import Actor

class HttpServerActor(Actor):
    def __init__(self, *args, **kwargs):
        Actor.__init__(self, *args, **kwargs)
        self.__log = getLogger('pulsar2.HttpServerActor')
        self._runner = None
        self._commands['update'] = self._update
        self._routes = {}

    def _update(self, path, content):
        """ Update server content
        """
        self.__log.debug('update: path = {path!r} content = {content!r}'.format(path=path, content=content))
        self._routes[path] = content

#    async def handle(self, request):
#        """
#        """
#        resp = []
#        for aid, agent in self._arbiter._managed_actors.items():
#            item = {
#                'name': '',
#                'aid': aid,
#                'info': agent.info(),
#            }
#            resp.append(item)
#        return web.json_response(resp)

    async def _start(self):
        """ Start Web-server
        """
        app = web.Application()
        app.add_routes([
#            web.get('/', self.handle),
        ])
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, '0.0.0.0', 8080)
        await site.start()

    async def _stop(self):
        """ Stop Web-server
        """
        await self._runner.cleanup()

    async def run(self):
#        self._loop.create_task()
        self.__log.debug("Start")
        await self._start()
