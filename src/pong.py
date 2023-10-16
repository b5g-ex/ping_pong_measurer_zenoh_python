from typing import Any, Iterator
import logging

import zenoh
from zenoh.session import Session

class Pong():
    def __init__(self, 
                 node_id: int, 
                 session: Session, 
                 ) -> None:

        self._node_id = node_id
        self.session = session
        self._ping_key = "ping_topic" + str(node_id)
        self._pong_key = "pong_topic" + str(node_id)

        self.publisher = self.session.declare_publisher(self._pong_key)

        self.subscriber = self.session.declare_subscriber(
            self._ping_key, 
            self.callback
            )

    def callback(self, message:str):
        self.pong(message)

    def pong(self, message:str):
        self.publisher.put(message)
