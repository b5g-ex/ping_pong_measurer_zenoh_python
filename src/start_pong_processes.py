import argparse
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

def start_pong_serving(node_id: int)-> None:
    # session を各pongノードで作成する (cf. start_pong_serving_session)
    session = zenoh.open()
    pong_node = Pong(node_id, session)
    pong_node.start()

def start_pong_serving_session(node_id: int, session: Session)-> None:
    pong_node = Pong(node_id, session)
    pong_node.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run pong process')
    parser.add_argument('--node', type=int, default=5, help='the number of Pong Node (default: 5)')


    args = parser.parse_args()
    node_num = args.node


    with concurrent.futures.ProcessPoolExecutor() as executor:        
        results = executor.map(start_pong_serving, list(range(node_num)))

    

    