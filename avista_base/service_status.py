from enum import Enum


class ServiceStatus(Enum):
    IDLE = 0
    INITIALIZING = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 4
    ERROR = 5
