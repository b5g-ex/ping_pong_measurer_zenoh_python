import concurrent.futures
import functools
from typing import List, Iterator

import zenoh
from zenoh.session import Session

import ping
import pong
from ping import Ping
from pong import Pong

def start_pong_processes(
        num_nodes: int
        ) -> None:
    session = zenoh.open()
    pong_iter = (pong.Pong(i, session) 
                 for i in range(num_nodes))
    return None

def start_pong_serving(node_id: int):
    session = zenoh.open()
    pong_node = Pong(node_id, session)
    pong_node.start()
    

if __name__ == "__main__":
    node_num = 1
    session = zenoh.open()

    with concurrent.futures.ProcessPoolExecutor() as executor:        
        results = executor.map(start_pong_serving, list(range(node_num)))

    for result in results:
        print(type(result))

    