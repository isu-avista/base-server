from gunicorn.app.base import BaseApplication


class AvistaApp(BaseApplication):

    def init(self, parser, opts, args):
        super().init(parser, opts, args)

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        """This loads the gunicorn configurations for the gunicorn BaseApplication that is inherited from"""
        cfg = dict([(key, value) for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None])
        for key, value in cfg.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """This simply returns the flask application for the BaseApplication to use"""
        return self.application