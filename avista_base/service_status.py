from enum import Enum


class ServiceStatus(Enum):
    """Enum representing the various states of the service"""

    IDLE = 0
    INITIALIZING = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 4
    ERROR = 5

    def __repr__(self):
        """An unambiguous representation of ServiceStatus"""
        return f"Service Status: {self.name}"

    def __str__(self):
        """A readable repreentation of Service Status"""
        return f"{self.name.lower().capitalize()}"

    @staticmethod
    def from_str(label):
        """Provides an instance of the Service Status for the given string

        Args:
            label (str): String representation of Service Status

        Returns:
            ServiceStatus: literal of ServiceStatus

        Raises:
            NotImplementedError: If value is not a defined enum literal of ServiceStatus
        """
        if label in ('IDLE', 'idle', 'Idle'):
            return ServiceStatus.IDLE
        elif label in ('ERROR', 'error', 'Error'):
            return ServiceStatus.ERROR
        elif label in ('INITIALIZING', 'initializing', 'Initializing'):
            return ServiceStatus.INITIALIZING
        elif label in ('STARTING', 'starting', 'Starting'):
            return ServiceStatus.STARTING
        elif label in ('STOPPING', 'stopping', 'Stopping'):
            return ServiceStatus.STOPPING
        elif label in ('RUNNING', 'running', 'Running'):
            return ServiceStatus.RUNNING
        else:
            raise NotImplementedError
