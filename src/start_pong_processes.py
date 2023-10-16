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
        num_nodes: int, 
        session: Session
        ) -> None:
    pong_iter = (pong.Pong(i, session) 
                 for i in range(num_nodes))
    return None

if __name__ == "__main__":
    node_num = 5
    session = zenoh.open()
    with concurrent.futures.ProcessPoolExecutor() as executor:        
        results = executor.map(functools.partial(start_pong_processes, session = session), [i for i in range(node_num)])