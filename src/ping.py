from collections.abc import Callable, Iterable, Mapping
from typing import Any
import zenoh, threading
from zenoh.session import Publisher

class Ping(threading.Thread):
    def __init__(self, node_id: int, ping_max: int = 10):
        self._node_id = node_id
        self._ping_max = ping_max
        self._counter = 0
        threading.Thread.__init__(self, name ='ping')

    def __str__(self):
        return 'ping multithreading'
    
    def get_ping_max(self):
        return self._ping_max
    
    def get_node_id(self):
        return self._node_id
    
    def callback(self, node_id: int, publisher: Publisher, message: str):
        return 
    
    # def run(self):



if __name__ == "__main__":
    session = zenoh.open()
    key = 'myhome/kitchen/temp'
    pub = session.declare_publisher(key)
    while True:
        t = read_temp()
        buf = f"{t}"
        print(f"Putting Data ('{key}': '{buf}')...")
        pub.put(buf)
        time.sleep(1)