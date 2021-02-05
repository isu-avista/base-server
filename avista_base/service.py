from abc import ABC, abstractmethod
from avista_base.service_status import ServiceStatus
from avista_base import auth
from avista_base import api
from avista_base import config
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from multiprocessing import Process
import multiprocessing
from avista_data.user import User
import avista_data
from gunicorn.app.base import BaseApplication
import logging
import os


class Service(ABC, BaseApplication):
    """Represents the base service class

    Attributes:
        _status (ServiceStatus): The current status of the service
        _config (dict): The app configuration
        application (Flask): The Flask app
        options (dict): Gunicorn options
        _name (str): The service name
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """ Static access method

                Returns:
                    The singleton instance of IoTServer
                """
        if Service._instance is None:
            cls()
        return Service._instance

    @classmethod
    def number_of_workers(cls):
        return (multiprocessing.cpu_count() * 2) + 1

    def __init__(self, options=None):
        """Constructs a new service the current app with the given name """
        if Service._instance is not None:
            raise Exception("This class is a singletion!")
        else:
            Service._instance = self
        self._status = ServiceStatus.IDLE
        self._config = None
        self._config_path = Path(os.environ.get("CONFIG_PATH"))
        self._config_file = 'config.yml'
        self._flask_config = None
        self._flask_config_file = 'flask.yml'
        self._log_path = Path(os.environ.get("LOG_PATH"))
        self._log_file = 'server.log'
        self.application = None
        self.options = options or {}
        self._name = __name__
        self._proc = None
        self._jwt = None
        super().__init__()

    def _init(self):
        """Initializes the service"""
        self._setup_logging()
        logging.info("Initializing")
        self._status = ServiceStatus.INITIALIZING
        self._load_config()
        self._load_flask_config()
        self._create_app()
        self._setup_database()
        self._setup_endpoints()

    def _setup_logging(self):
        logging.basicConfig(filename=self._log_path / self._log_file, level=logging.DEBUG)

    def _load_config(self):
        """Loads the flask configuration"""
        logging.info("Loading Service Configuration")

        self._config = config.load(self._config_path / self._config_file)

    def _load_flask_config(self):
        """ """
        logging.info("Loading Flask Configuration")

        self._flask_config = config.load(self._config_path / self._flask_config_file)

    def _create_app(self):
        """Constructs the flask app"""
        logging.info("Creating Flask App")

        self.application = Flask(self._name)
        self.application.config.from_mapping(self._flask_config)
        self.application.app_context().push()
        CORS(self.application, resources={r"/*": {"origins": "*"}})
        self._jwt = JWTManager(self.application)

    def _setup_endpoints(self):
        logging.info("Registering Flask Endpoints")
        self.application.register_blueprint(auth.bp)
        self.application.register_blueprint(api.bp)

        @self._jwt.user_claims_loader
        def add_claims_to_access_token(identity):
            user = User.find_user(identity)
            return {'role': str(user.get_role())}

    def _setup_database(self):
        avista_data.data_manager.init()
        avista_data.populate_initial_data()

    def start(self):
        """Starts the service"""
        self._init()
        logging.info("Starting")
        self._status = ServiceStatus.STARTING
        hostname = self._config['service']['host']
        portnum = int(self._config['service']['port'])
        self._proc = Process(target=self.application.run, kwargs={'host': hostname, 'port': portnum})
        self._proc.start()

        logging.info("Running")
        self._status = ServiceStatus.RUNNING

    def stop(self):
        """Stops the service"""
        logging.info("Stopping")
        self._status = ServiceStatus.STOPPING

        self._proc.terminate()
        self._proc.join()

        self._status = ServiceStatus.IDLE

    def restart(self):
        """Restarts this service"""
        logging.info("Restarting")
        self.stop()
        self.start()

    def status(self):
        """Returns the current status of the service"""
        return self._status

    def get_config(self, section):
        """ retrieves the config for the given section

        Args:
            section (str): The name of the section of the config to retrieve

        Returns:
            a dictionary representing the subsection of the configuration

        Raises:
            Exception if the provided section is None, empty, or non-existant
        """
        if section is None or section == "" or section not in self._config.keys():
            raise Exception("section cannot be None or empty and must be in the config")
        return self._config[section]

    def set_config(self, section, config_data):
        """ Updates the config section with the provided configuration information

        Args:
            section (str): the section to update

            config_data (dict): the new data for the section

        Raises:
            Exception if the provided section is None or empty or the provided data is None
        """
        if section is None or section == "":
            raise Exception("section cannot be None or empty")
        if config_data is None:
            raise Exception("data cannot be None")
        self._config[section] = config_data
        config.save(self._config, self._config_path / self._config_file)

    @abstractmethod
    def check_status(self):
        pass

    def get_log(self):
        """ returns the last five lines of the log

        Returns:
            a dictionary containing a single entry "log" which is the last five lines of the log file
        """
        with open(self._log_path / self._log_file, "r") as a_file:
            lines = a_file.readlines()
            return dict(log='\n'.join(lines[-5:]))

    def load_config(self):
        cfg = dict([(key, value) for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None])
        for key, value in cfg.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
