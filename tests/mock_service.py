from avista_base.service import Service
from multiprocessing import Process


class MockService(Service):

    def __init__(self):
        """ instantiate the app """
        super().__init__()

    def start(self):
        super().start()
        self._proc = Process(target=self._app.run, kwargs={'host': self.hostname, 'port': self.port})
        self._proc.start()

    def check_status(self):
        pass
