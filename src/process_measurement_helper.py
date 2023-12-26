import concurrent.futures
import datetime
import functools
import os

import zenoh
from zenoh.session import Session, Sample

import ping_pong_measurer_zenoh_python as pzp
from ping import Ping
from measurer import Measurer, State


# ping pong using Zenoh-python in multithread

class PingThread():
    def __init__(self, session: Session, message: str, measurer: Measurer):
        self._session = session
        self._message = message
        self._measurer = measurer
        # self._node_id = node_id : start_ping_pong に与える
    
    def start_ping_pong(self, node_id: int):
        ping_node = Ping(node_id, self._session, self._measurer)
        ping_node.start(self._message)

class MeasureThread():
    def __init__(self, node_id: int):
        self._ping_node_id = node_id
    


if __name__ == "__main__":
    measurement_times = 10
    node_num = 1
    payload_bytes = 100
    message = 'a' * payload_bytes
    session = zenoh.open()

    start_pp = PingThread(session, message)
    # TODO: 
    # t_delta = datetime.timedelta(hours=9)
    # JST = datetime.timezone(t_delta, 'JST')
    # now = datetime.datetime.now(JST)
    # now_string = now.strftime('%Y%m%d%H%M%S')
    # TODO: data_folder_path = os.path.join("./data/",now_string)
    # TODO: Measurer の作成 measurers = [Measururer(state(node_id = i, data_directory_path = data_folder_path)) for i in range(node_num)]

    for i in range(measurement_times):
    # ThreadPoolExecutor の場合
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # publish ping message concurrently
            # results = executor.map(functools.partial(pzp.start_ping_pong, message = message), list(range(node_num)))
            results = executor.map(start_pp.start_ping_pong, list(range(node_num)))

        print(f">>>>>>>>>> #{i+1}/#{measurement_times}")

    print("end ping loop")

    pzp.stop_ping_measurer() # measurer の起動はThreadPoolExecutorの中で（このオーバーヘッドが大きいと予想するので）
    pzp.stop_ping_processes()
    pzp.stop_os_info_measurement()