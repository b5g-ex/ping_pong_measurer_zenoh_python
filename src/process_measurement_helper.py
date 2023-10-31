import concurrent.futures
import logging
import functools

import zenoh

import ping_pong_measurer_zenoh_python as pzp
from ping import Ping


# ping pong using Zenoh-python in multithread

class PingPong():
    def __init__(self, session, message):
        self._session = session
        self._message = message
    
    def start_ping_pong(self, node_id):
        ping_node = Ping(node_id, self._session)
        ping_node.start(self._message)

if __name__ == "__main__":
    measurement_times = 10
    node_num = 1
    payload_bytes = 100
    message = 'a' * payload_bytes
    session = zenoh.open()

    start_pp = PingPong(session, message)

    for i in range(measurement_times):
    # ThreadPoolExecutor の場合
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # publish ping message concurrently
            # results = executor.map(functools.partial(pzp.start_ping_pong, message = message), list(range(node_num)))
            results = executor.map(start_pp.start_ping_pong, list(range(node_num)))

        print(f">>>>>>>>>> #{i+1}/#{measurement_times}")

    print("end ping loop")

    pzp.stop_ping_measurer()
    pzp.stop_ping_processes()
    pzp.stop_os_info_measurement()