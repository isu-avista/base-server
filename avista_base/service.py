from abc import ABC, abstractmethod
from multiprocessing import Process
from avista_base.service_status import ServiceStatus
from avista_base import auth
from avista_base import api
from avista_base import config
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from avista_data.user import User
import avista_data
import logging
import os


class Service(ABC):
    """Represents the base service class

    Attributes:
        _status (ServiceStatus): The current status of the service
        _config (dict): The app configuration
        _app (Flask): The Flask app
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

    def __init__(self):
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
        self.hostname = '0.0.0.0'
        self.port = '5000'
        self._app = None
        self._name = __name__
        self._proc = None
        self._jwt = None

    def initialize(self):
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
        """Loads flask configuration from file"""
        logging.info("Loading Flask Configuration")

        self._flask_config = config.load(self._config_path / self._flask_config_file)
        uri = self.__generate_db_uri()
        self._flask_config['SQLALCHEMY_DATABASE_URI'] = uri

    def __generate_db_uri(self):
        type = ip = port = user = passwd = db = ""
        for item in self._config['dbdata']:
            if item['item'] == "DBMS Type":
                type = item['type']
            elif item['item'] == "DBMS IP Address":
                ip = item['value']
            elif item['item'] == "DBMS Port":
                port = item['value']
            elif item['item'] == "DBMS Username":
                user = item['value']
            elif item['item'] == "DBMS Password":
                passwd = item['value']
            elif item['item'] == "DBMS DB Name":
                db = item['value']
        return f'{type}://{user}:{passwd}@{ip}:{port}/{db}'

    def _create_app(self):
        """Constructs the flask app"""
        logging.info("Creating Flask App")

        self._app = Flask(self._name)
        self._app.config.from_mapping(self._flask_config)
        self._app.app_context().push()
        CORS(self._app, resources={r"/*": {"origins": "*"}})
        self._jwt = JWTManager(self._app)

    def _setup_endpoints(self):
        logging.info("Registering Flask Endpoints")
        self._app.register_blueprint(auth.bp)
        self._app.register_blueprint(api.bp)

        @self._jwt.user_claims_loader
        def add_claims_to_access_token(identity):
            user = User.find_user(identity)
            return {'role': str(user.get_role())}

    def _setup_database(self):
        avista_data.data_manager.init()
        avista_data.populate_initial_data()

    def start(self):
        """Starts the service"""
        logging.info("Starting")
        self._status = ServiceStatus.STARTING
        self.hostname = self._config['service']['host']
        self.port = int(self._config['service']['port'])

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

    def get_hostname(self):
        return self.hostname

    def get_port(self):
        return self.port

    def get_app(self):
        return self._app
