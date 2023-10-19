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

if __name__ == "__main__":
    node_num = 1
    with concurrent.futures.ProcessPoolExecutor() as executor:        
        results = executor.map(functools.partial(start_pong_processes), [i for i in range(node_num)])

    for result in results:
        print(type(result))