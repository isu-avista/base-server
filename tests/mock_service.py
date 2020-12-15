from avista_base.service import Service


class MockService(Service):

    def __init__(self):
        """ instantiate the app """
        super().__init__()

    def check_status(self):
        pass
