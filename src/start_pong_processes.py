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

def start_pong_serving(pong_node: Pong):
    pong_node.start()
    

if __name__ == "__main__":
    node_num = 1
    session = zenoh.open()
    pong_nodes = [Pong(x, session) for x in range(node_num)]
    with concurrent.futures.ProcessPoolExecutor() as executor:        
        results = executor.map(start_pong_serving, pong_nodes)

    for result in results:
        print(type(result))

    