from time import perf_counter_ns as timer
from typing import Any, Iterator, List
import logging
from queue import Queue
import zenoh
from zenoh.session import Session, Sample

from measurer import Measurer

class Ping():
    def __init__(self, 
                 node_id: int, 
                 session: Session, 
                 measurer: Measurer,
                 ping_max: int = 1
                 ) -> None:
        self.queue = Queue()
        self._node_id = node_id
        self.session = session
        self.measurer = measurer
        self._ping_max = ping_max
        self._counter = 0
        self._ping_key = "ping_topic/" + str(node_id)
        self._pong_key = "pong_topic/" + str(node_id)

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
            self.queue.put("end")
            

    def ping(self, message:str):
        self.publisher.put(message)

    def start(self,message:str):
        self.ping(message)
        self.queue.get()


class PingManyToOneToOne():
    """
    ping class for many (ping) to one (zenoh topic) to one (pong) pingpong comm.

    note: number of pingpong comm. must be 1.
    """
    def __init__(self, 
                 node_id: int, 
                 session: Session, 
                 measurer: Measurer,
                 node_num: int
                 ) -> None:
        self.queue = Queue()
        self._node_id = node_id
        self.session = session
        self.measurer = measurer
        self._node_num = node_num
        self._counter = 0
        self._ping_key = "ping_topic"
        self._pong_key = "pong_topic"

        self.publisher = session.declare_publisher(self._ping_key)

        self.subscriber = session.declare_subscriber(
            self._pong_key, 
            self.callback
            )

    def callback(self, sample: Sample):
        if self._counter < self._node_num:
            print(f"ping recv {self._node_id}")
            self._counter += 1
        else:
            self.queue.put("end")
            

    def ping(self, message:str):
        self.publisher.put(message)
        print(f"ping {self._node_id}")

    def start(self,message:str):
        self.ping(message)
        self.queue.get()