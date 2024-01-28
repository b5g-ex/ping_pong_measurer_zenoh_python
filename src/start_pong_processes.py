import argparse
import concurrent.futures
from functools import partial
from typing import List, Iterator

import zenoh
from zenoh.session import Session

import ping
import pong
from ping import Ping
from pong import Pong, PongManyToOne, PongManyToOneToOne

# def start_pong_processes(
#         num_nodes: int
#         ) -> None:
#     session = zenoh.open()
#     pong_iter = (pong.Pong(i, session) 
#                  for i in range(num_nodes))
#     return None


def start_pong_serving(node_id: int)-> None:
    # session を各pongノードで作成する (cf. start_pong_serving_session)
    session = zenoh.open()
    pong_node = Pong(node_id, session)
    pong_node.start()

def start_pong_many2one_serving(node_num: int)-> None:
    session = zenoh.open()
    pong_node = PongManyToOne(node_num, session)
    pong_node.start()

def start_pong_many2one2one_serving(node_num: int)-> None:
    session = zenoh.open()
    pong_node = PongManyToOneToOne(node_num, session)
    pong_node.start()

def start_pong_serving_session(node_id: int, session: Session)-> None:
    print("pong")
    pong_node = Pong(node_id, session)
    pong_node.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run pong process')

    # for many to many to one pingpong comm.
    parser.add_argument('--m2one', type=bool, default=False, help='run only one pong for many to many to one ping pong')
    parser.add_argument('--pingnode', type=int, default=5, help='the number of P"i"ng Node (default: 5)')

    # for many to one to one pingpong comm.
    parser.add_argument('--m2one2one', type=bool, default=False, help='run only one pong for many to one to one ping pong')

    # for many to many to many pingpong comm.
    parser.add_argument('--node', type=int, default=1, help='the number of Pong Node (default: 5)')


    args = parser.parse_args()
    m2one = args.m2one
    m2one2one = args.m2one2one
    ping_node_num = args.pingnode
    node_num = args.node

    session = zenoh.open()
    start_pong_serving_w_session = partial(start_pong_serving_session, session = session)

    if m2one:
        start_pong_many2one_serving(ping_node_num)
    elif m2one2one:
        start_pong_many2one2one_serving(ping_node_num)
    else: 
        print("else")
        with concurrent.futures.ProcessPoolExecutor(max_workers=node_num) as executor: 
            print('a')
            results = executor.map(start_pong_serving_w_session, list(range(node_num)))

        print("[bug] end pong")
    

    