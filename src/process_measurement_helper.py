import argparse
import concurrent.futures
import datetime
import functools
import os
from time import perf_counter_ns as timer
from typing import Any, Iterator, List

import zenoh
from zenoh.session import Session, Sample

import ping_pong_measurer_zenoh_python as pzp
from ping import Ping, PingManyToOneToOne
from measurer import Measurer, State


# ping pong using Zenoh-python in multithread

class PingThread():
    def __init__(self, ping_max: int, session: Session, messages: List[str], measurers: List[Measurer]):
        self._ping_max = ping_max
        self._session = session
        self._messages = messages
        self._measurers = measurers
    
    def start_ping_pong(self, node_id: int):
        measurer = self._measurers[node_id]
        ping_node = Ping(node_id, self._session, measurer, self._ping_max)

        measurer.start_measurement(timer()/1e6)
        # perf_counter_ns は nano second
        # 1 millisecond = 1000,000 nanosecond
        ping_node.start(self._messages[node_id])
        measurer.stop_measurement(timer()/1e6)


class PingThreadManyToOneToOne():
    def __init__(self, node_num: int, session: Session, messages: List[str], measurers: List[Measurer]):
        self._node_num = node_num
        self._session = session
        self._messages = messages
        self._measurers = measurers
    
    def start_ping_pong(self, node_id: int):
        measurer = self._measurers[node_id]
        ping_node = PingManyToOneToOne(node_id, self._session, measurer, self._node_num)

        measurer.start_measurement(timer()/1e6)
        # perf_counter_ns は nano second
        # 1 millisecond = 1000,000 nanosecond
        ping_node.start(self._messages[node_id])
        measurer.stop_measurement(timer()/1e6)

    
def get_now_string() -> str:
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    now_string = now.strftime('%Y%m%d%H%M%S')
    return now_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run pong process')

    parser.add_argument('--m2one2one', type=bool, default=False, help='')

    parser.add_argument('--node', type=int, default=5, help='the number of Pong Node (default: 5)')
    parser.add_argument('--mt', type=int, default=100, help='the number of Measurement (default: 100)')
    parser.add_argument('--pb', type=int, default=100, help='the payload byte of pingpong message (default: 100)')
    parser.add_argument('--pt', type=int, default=1, help='the number of pingpong (default: 1)')
    

    args = parser.parse_args()
    m2one2one = args.m2one2one
    node_num = args.node
    measurement_times = args.mt
    payload_bytes = args.pb
    pingpong_times = args.pt
    message = 'a' * payload_bytes
    messages = [message for _ in range(node_num)]
    session = zenoh.open()

    
    mode = "m11" if m2one2one else "mm1"
    now_str = get_now_string()
    data_folder_path = os.path.join(f"./data/",f"{mode}_pc{node_num}_pb{payload_bytes}_mt{measurement_times}_pt{pingpong_times}_{now_str}")
    try:
        os.makedirs(data_folder_path)
    except FileExistsError:
        pass


    measurers = [Measurer(State(node_id = i),  data_directory_path = data_folder_path) for i in range(node_num)]


    if m2one2one:
        start_pp = PingThreadManyToOneToOne(node_num, session, messages, measurers)
    else:
        start_pp = PingThread(pingpong_times, session, messages, measurers)
    

    for m_time in range(measurement_times):
        
    # ThreadPoolExecutor の場合
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # publish ping message concurrently
            results = executor.map(start_pp.start_ping_pong, list(range(node_num)))

    print("end ping loop")

    pzp.stop_ping_measurer(measurers) # measurer の測定開始はThreadPoolExecutorの中で（このオーバーヘッドが大きいと予想するので）
    pzp.stop_ping_processes()
    # pzp.stop_os_info_measurement()