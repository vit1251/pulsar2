
from logging import getLogger
from asyncio import get_event_loop, new_event_loop
from uuid import uuid4

from ._CommandError import CommandError

class Arbiter(object):
    """ Arbiter a very special actor which controls the life of all actors

    To use actors in pulsar you need to start the Arbiter, a very special actor which controls the life of all
    actors spawned during the execution of your code.

    """
    def __init__(self, loop=None):
        self.__log = getLogger('pulsar2.Arbiter')
        self._loop = loop or get_event_loop() or new_event_loop()
        self._managed_actors = {}

    def is_running(self):
        """
        """
        return self._loop.is_running()

    def start(self):
        """ Start
        """
        self._loop.run_forever()

    def stop(self):
        """ Stop
        """
        self._loop.stop()

    def get_actor(self, aid: str):
        """ Given an actor unique id return the actor or use actor proxy.
        """
        result = self._managed_actors.get(aid, None)
        return result

    @staticmethod
    def create_aid():
        aid = uuid4()
        result = str(aid)
        return result

    def identity(self, actor):
        return actor.aid

    def spawn(self, actor, aid=None):
        """
        """
        aid = aid or self.create_aid()
        self.__log.debug("spawn: actor = {actor!r} aid = {aid!r}".format(actor=actor, aid=aid))
        a = actor(arbiter=self)
        a._aid = aid
        self._managed_actors[aid] = a
        a.start()

    def send(self, sender, target, action, *args, **kwargs):
        """ An Actor communicates with another Actor by sending an action to perform.
        This action takes the form of a command name and optional positional and key-valued parameters.
        """
        self.__log.debug("send: target = {target!r} action = {action!r}".format(target=target, action=action))
        actor = self.get_actor(target)
        if actor:
            self._loop.create_task(actor._mailbox.put({"sender": sender, "action": action, "args": args, "kwargs": kwargs}))
        else:
            self.__log.warn('Cannot execute {action!r} in {sender!r}. Unknown actor {target!r}.'.format(action=action, sender=sender, target=target))

    def kill_actor(self, aid, timeout=5):
        """ Kill an actor with id ``aid``.
        """
        actor = self.get_actor(target)
        if actor:
            actor.stop()
        else:
            self.__log.warn('No actor exists')
