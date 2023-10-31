from typing import Any, Iterator
import logging
from queue import Queue

import zenoh
from zenoh.session import Session, Sample


class Ping():
    def __init__(self, 
                 node_id: int, 
                 session: Session, 
                 ping_max: int = 10
                 ) -> None:
        self.queue = Queue()
        self._node_id = node_id
        # self.session = session : session はpickle できない
        self._ping_max = ping_max
        self._counter = 0
        self._ping_key = "ping_topic" + str(node_id)
        self._pong_key = "pong_topic" + str(node_id)

        self.publisher = session.declare_publisher(self._ping_key)

        self.subscriber = session.declare_subscriber(
            self._pong_key, 
            self.callback
            )

    def callback(self, sample: Sample):
        
        message = sample.payload.decode('utf-8')
        if self._counter < self._ping_max:
            self.ping(message)
            self._counter += 1
        else:
            logging.info(f"ping {self._node_id} reached ping_max")
            print(f"ping {self._node_id} reached ping_max")
            self.queue.put("end")
            

    def ping(self, message:str):
        self.publisher.put(message)

    def start(self,message:str):
        self.ping(message)
        self.queue.get()
