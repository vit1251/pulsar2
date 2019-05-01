
from logging import getLogger

from ._Actor import Actor

class DiscoverProtocol(object):
    def __init__(self, actor):
        self.__log = getLogger('pulsar2.DiscoverActor.DiscoverProtocol')
        self._actor = actor

    def connection_made(self, transport):
        pass

    def datagram_received(self, data, addr):
        """ Recv discover packet
        """
        message = data.decode()
        self.__log.debug('Received %r from %s' % (message, addr))
        self.__log.debug('Send %r to %s' % (message, addr))
        #self.transport.sendto(data, addr)
        #
        self._actor._nodes[addr] = data

class DiscoverActor(Actor):
    def __init__(self, *args, **kwargs):
        Actor.__init__(self, *args, **kwargs)
        self.__log = getLogger('pulsar2.HttpServerActor')
        self._nodes = {}

    async def run(self):
        #
        transport, protocol = await self._loop.create_datagram_endpoint(
            lambda: DiscoverProtocol(self),
            local_addr=('0.0.0.0', 9999)
        )
        #
        await Actor.run(self)
