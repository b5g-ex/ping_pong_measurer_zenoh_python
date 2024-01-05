from typing import Any, Iterator
import logging
import time

import zenoh
from zenoh.session import Session, Sample

class Pong():
    def __init__(self, 
                 node_id: int, 
                 session: Session, 
                 ) -> None:

        self._node_id = node_id
        # self.session = session : session はpickleできない？
        self._ping_key = "ping_topic" + str(node_id)
        self._pong_key = "pong_topic" + str(node_id)

        self.publisher = session.declare_publisher(self._pong_key)

        self.subscriber = session.declare_subscriber(
            self._ping_key, 
            self.callback
            )

    def callback(self, sample: Sample):
        message = sample.payload.decode('utf-8')
        self.pong(message)

    def pong(self, message:str):
        self.publisher.put(message)

    def start(self):
        while True:
            logging.info("pong: serving")
            time.sleep(5)

if __name__ == "__main__":
    session = zenoh.open()
    pong = Pong(0, session)

    pong.sample()
