import concurrent.futures
import logging
import functools

import zenoh

import ping_pong_measurer_zenoh_python as pzp


# ping pong using Zenoh-python in multiprocess

if __name__ == "__main__":
    measurement_times = 10
    node_num = 1
    payload_bytes = 100
    message = 'a' * payload_bytes

    # iterator of ping.Ping
    iter_ping = pzp.start_ping_processes(node_num) 
    pzp.start_ping_measurer()


    for i in range(measurement_times):
    # ProcessPoolExecutor の場合
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # publish ping message concurrently
            results = executor.map(functools.partial(pzp.start_ping_pong, message), iter_ping)
        
            print(f">>>>>>>>>> #{i}/#{measurement_times}")

    pzp.stop_ping_measurer()
    pzp.stop_ping_processes()
    pzp.stop_os_info_measurement()