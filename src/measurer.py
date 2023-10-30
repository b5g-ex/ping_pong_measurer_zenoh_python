from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterator, List
import logging

import zenoh
from zenoh.session import Session, Sample

@dataclass
class Measurement():
    measurement_time: datetime
    send_time: int
    recv_time: int

@dataclass
class State():
    ping_counts:int =  0
    measurements: List[Measurement] = []
    data_directory_path: str =  ""
    process_index: int = 0

class Measurer():
    node_id_prefix = 'ping_node'
    def __init__(self, state: State) -> None:
        self.state = state

    def get_ping_counts(self) -> int:
        return self.state.ping_counts

    def increment_ping_counts(self) -> int:
        self.state.ping_counts += 1

    def reset_ping_counts(self) -> None:
        self.state.ping_counts = 0
    
    def start_measurement(self) -> None:
        pass

    def stop_measurement(self) -> None:
        pass

    def get_measurement_time(self) -> None:
        return self.state.measurements

    def terminate(self) -> None:
        pass


