
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from logging import getLogger
from asyncio import sleep
from json import dumps

from ipaddress import IPv4Address, IPv4Network

from ._Actor import Actor

class DiscoverProtocol(object):
    def __init__(self, actor):
        self.__log = getLogger('pulsar2.DiscoverActor.DiscoverProtocol')
        self._actor = actor
        self._transport = None

    def connection_made(self, transport):
        self._transport = transport

    def datagram_received(self, data, addr):
        """ Recv discover packet
        """
        message = data.decode()
        self.__log.debug('Received %r from %s' % (message, addr))
        self.__log.debug('Send %r to %s' % (message, addr))
        #
        self._actor._nodes[addr] = data

class DiscoverActor(Actor):
    def __init__(self, *args, **kwargs):
        Actor.__init__(self, *args, **kwargs)
        self.__log = getLogger('pulsar2.DiscoverActor')
        self._nodes = {}
        self._periodic_notify = False
        self._transport = None
        #
        self._commands['manage'] = self._manage

    def notify(self, network):
        self.__log.debug("notify: network = {network!r}".format(network=network))
        cs = socket(AF_INET, SOCK_DGRAM)
        #cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        addr = (network, 9999)
        params = {
            'user-agent': 'pulsar2',
            'version': '1.0',
        }
        content = dumps(params)
        packet = content.encode('latin1')
        cs.sendto(packet, addr)
        cs.close()

    def _manage(self, addr=None, mask='255.255.255.0', ident=None, interval=10.0):
        """ Start discovery on network
        """
        host = IPv4Address(addr)
        net = IPv4Network(addr + '/' + mask, False)
        #self.__log.debug('addr = {addr!r}'.format(addr=addr))
        #print('Mask:', MASK)
        #print('Subnet:', ipaddress.IPv4Address(int(host) & int(net.netmask)))
        #print('Host:', ipaddress.IPv4Address(int(host) & int(net.hostmask)))
        self.__log.debug('broadcast_address = {broadcast_address!r}'.format(broadcast_address=net.broadcast_address))

        #
        network = str(net.broadcast_address)

        # Start update
        self._loop.create_task(self._discovery_network_start(network=network, interval=interval))

    async def _discovery_network_start(self, network=None, interval=10.0):
        """ Start discovery network
        """

        transport, protocol = await self._loop.create_datagram_endpoint(
            lambda: DiscoverProtocol(self),
            local_addr=('0.0.0.0', 9999)
        )

        self._periodic_notify = True
        while self._periodic_notify:
            self.__log.debug('Disocvery: network = {network!r}'.format(network=network))
            self.notify(network)
            await sleep(interval)

    async def _discovery_network_stop(self):
        """ Stop discovery network
        """
        # TODO - implement network ...
