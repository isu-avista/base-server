import abc
import logging
from avista_base.service_status import ServiceStatus
from avista_base import config
from pathlib import Path
from flask import Flask
import avista_data
import os


class Service(abc.ABC):
    """ """

    def __init__(self, app, name):
        """ """
        self._status = ServiceStatus.IDLE
        self._config = None
        self._app = app
        self._name = name

    def init(self):
        """ """
        logging.info("Initializing")
        self._status = ServiceStatus.INITIALIZING
        self._load_config()
        self._create_app()

    def _load_config(self):
        """ """
        logging.info("Loading Config")

        config_dir = Path(os.environ.get('CONFIG_PATH'))
        self._config = config.load(config_dir / "config.yml")

    def _create_app(self):
        """ """
        self._app = Flask(self._name)
        self._app.config.from_mapping(self._config)
        avista_data.init(self._app)

    def start(self):
        """ """
        logging.info("Starting")
        self._status = ServiceStatus.STARTING
        self.init()
        self.run()

    def run(self):
        """ """
        logging.info("Running")
        self._status = ServiceStatus.RUNNING

    def stop(self):
        """ """
        logging.info("Stopping")
        self._status = ServiceStatus.STOPPING

        self._status = ServiceStatus.IDLE

    def restart(self):
        """ """
        logging.info("Restarting")
        self.stop()
        self.start()

    def status(self):
        """ """
        return self._status
