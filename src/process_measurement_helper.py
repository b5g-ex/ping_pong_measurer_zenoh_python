import concurrent.futures
import datetime
import functools
import os
from time import perf_counter_ns as timer

import zenoh
from zenoh.session import Session, Sample

import ping_pong_measurer_zenoh_python as pzp
from ping import Ping
from measurer import Measurer, State


# ping pong using Zenoh-python in multithread

class PingThread():
    def __init__(self, session: Session, messages: list[str], measurers: list[Measurer]):
        self._session = session
        self._messages = messages
        self._measurers = measurers
    
    def start_ping_pong(self, node_id: int):
        measurer = self._measurers[node_id]
        ping_node = Ping(node_id, self._session, measurer)

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
    measurement_times = 10
    node_num = 1
    payload_bytes = 100
    message = 'a' * payload_bytes
    messages = [message for _ in range(node_num)]
    session = zenoh.open()

    
    now_str = get_now_string()
    data_folder_path = os.path.join(f"../data/",f"{now_str}_pc{node_num}_pb{payload_bytes}_mt{measurement_times}")
    try:
        os.makedirs(data_folder_path)
    except FileExistsError:
        pass


    measurers = [Measurer(State(node_id = i),  data_directory_path = data_folder_path) for i in range(node_num)]
    start_pp = PingThread(session, messages, measurers)
    

    for m_time in range(measurement_times):
        
    # ThreadPoolExecutor の場合
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # publish ping message concurrently
            results = executor.map(start_pp.start_ping_pong, list(range(node_num)))

        print(f">>>>>>>>>> #{m_time+1}/#{measurement_times}")

    print("end ping loop")

    pzp.stop_ping_measurer(measurers) # measurer の測定開始はThreadPoolExecutorの中で（このオーバーヘッドが大きいと予想するので）
    pzp.stop_ping_processes()
    pzp.stop_os_info_measurement()