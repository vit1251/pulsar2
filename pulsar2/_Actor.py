
from logging import getLogger
from os import getpid
from threading import current_thread
from asyncio import Queue

from ._ActorState import ActorState

class Actor(object):
    """ The base class for parallel execution in pulsar.

    In computer science, the **Actor model** is a mathematical model
    of concurrent computation that treats *actors* as the universal primitives
    of computation.
    In response to a message that it receives, an actor can make local
    decisions, create more actors, send more messages, and determine how
    to respond to the next message received.

    The current implementation allows for actors to perform specific tasks
    such as listening to a socket, acting as http server, consuming
    a task queue and so forth.
    """

    def __init__(self, arbiter, *args, **kwargs):
        self.__log = getLogger('pulsar2.Actor')
        self._arbiter = arbiter
        #
        self._state = ActorState.INITIAL
        self._name = None
        self._tid = current_thread().ident
        self._pid = getpid()
        self._loop = arbiter._loop
        self._aid = None
        #
        self._mailbox = Queue()
        self._commands = {}

    @property
    def info_state(self):
        return None # ActorStateDescription[self._state]

    @property
    def aid(self):
        return self._aid

    def start(self, exit=True):
        """ Called after spawn to start the actor's life.

        This is where logging is configured, the `mailbox` is
        registered, initialised and started.

        Calling this method more than once does nothing.
        """
        if self._state == ActorState.INITIAL:
            self._started = self._loop.time()
            self._exit = exit
            self._state = ActorState.STARTING
            #
            self._commands['stop'] = self.stop
            self._commands['ping'] = self.ping
            self._commands['info'] = self.info
            self._commands['echo'] = self.echo
            #
            self._loop.create_task(self.run())

    @property
    def unique_name(self):
        return '{name}.{aid}'.format(name=self._name, aid=self._aid)

    def ping(self, extra=False):
        """ Ping message
        """
        if extra:
            result = {
#                'recv_at': 
                'process_at': self._loop.time(),
            }
        else:
            result = 'pong'
        return result

    def echo(self, msg):
        return msg

    def info(self):
        """ Return a dictionary of information related to the actor status and performance.

        The dictionary contains the following entries:

        """
        result = {
            'name': self._name,
            'state': self.info_state,
            'actor_id': self.aid,
            'uptime':  self._loop.time() - self._started,
            'thread_id': self._tid,
            'process_id': self._pid,
        }
        return result

    def is_alive(self):
        pass

    def send(self, target, action, **kwargs):
        """
        """
        self._arbiter.send(self, target, action, **kwargs)

    async def run(self):
        self._running = True
        while self._running:
            msg = await self._mailbox.get()
            action = msg.get('action')
            args = msg.get('args', [])
            kwargs = msg.get('kwargs', {})
            method = self._commands.get(action)
            if callable(method):
                result = method(*args, **kwargs)
            else:
                self.__log.warn('Unable invoke {action!r} in {agent!r}.'.format(action=action, agent=self))

    def stop(self):
        """ Gracefully stop the Actor
        """
        self._running = False
        #self._mailbox.put({}) # TODO - close queue and raise an error in `run` ...
