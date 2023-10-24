import concurrent.futures
from typing import List, Iterator

import zenoh
from zenoh.session import Session

import ping
import pong
from ping import Ping
from pong import Pong

def start_ping_processes(
        num_nodes: int, 
        ping_max: int = 10
        ) -> Iterator[Ping]:
    
    session = zenoh.open()
    ping_iter = (ping.Ping(i, session, ping_max) 
                 for i in range(num_nodes))
    return ping_iter


def start_ping_measurer() -> None:
    pass

def start_ping_pong(node_id: int, message: str) -> None:
    # TODO: ping_max を引数に取る（Pingに与える）
    # session をノードごとにつくるバージョン　(cf. start_ping_pong_session)
    session = zenoh.open()
    ping_node = Ping(node_id, session)
    ping_node.ping(message)

def start_ping_pong_session(node_id: int, session: Session, message: str) -> None:
    # TODO: ping_max を引数に取る（Pingに与える）
    # session を全ノードで共有するバージョン　(cf. start_ping_pong)
    ping_node = Ping(node_id, session)
    ping_node.ping(message)

def stop_ping_measurer() -> None:
    pass

def stop_ping_processes() -> None:
    pass

def stop_os_info_measurement() -> None:
    pass

