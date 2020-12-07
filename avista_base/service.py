import abc
import logging
from avista_base.service_status import ServiceStatus
from avista_base import config
from pathlib import Path
from flask import Flask
import avista_data
import os


class Service(abc.ABC):
    """Represents the base service class

    Attributes:
        _status (ServiceStatus): The current status of the service
        _config (dict): The app configuration
        _app (Flask): The Flask app
        _name (str): The service name
    """

    def __init__(self, app, name):
        """Constructs a new service the given app with the given name

        Args:
            app (:obj: `Flask`): The flask app
            name (str): name of the service
        """
        self._status = ServiceStatus.IDLE
        self._config = None
        self._app = app
        self._name = name

    def init(self):
        """Initializes the service"""
        logging.info("Initializing")
        self._status = ServiceStatus.INITIALIZING
        self._load_config()
        self._create_app()

    def _load_config(self):
        """Loads the flask configuration"""
        logging.info("Loading Config")

        config_dir = Path(os.environ.get('CONFIG_PATH'))
        self._config = config.load(config_dir / "config.yml")

    def _create_app(self):
        """Constructs the flask app"""
        self._app = Flask(self._name)
        self._app.config.from_mapping(self._config)
        avista_data.init(self._app)

    def start(self):
        """Starts the service"""
        self.init()
        logging.info("Starting")
        self._status = ServiceStatus.STARTING

        self.run()

    def run(self):
        """Places the service into the running mode"""
        logging.info("Running")
        self._status = ServiceStatus.RUNNING

    def stop(self):
        """Stops the service"""
        logging.info("Stopping")
        self._status = ServiceStatus.STOPPING

        self._status = ServiceStatus.IDLE

    def restart(self):
        """Restarts this service"""
        logging.info("Restarting")
        self.stop()
        self.start()

    def status(self):
        """Returns the current status of the service"""
        return self._status
