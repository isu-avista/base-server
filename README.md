# Avista-Base-Server

## Description

This is the base server package upon which all other isu-avista service projects rely.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Credits](#credits)
4. [License](#license)

## Installation

To install this module us the following command:

```
pip3 install git+ssh://git@github.com/isu-avista/base-server.git
```

## Usage

To construct a new Service, you simply need to complete the following steps:

1. Extend `avista_base.service.Service` class and implement the following methods
   - __init__ and ensure that it calls the super version:
   ```python
   def __init__(self):
      super().__init__()
   ```
   - As you define your api blueprints you will need to add them to the `_setup_endpoints` method likeso
   ```python
   def _setup_endpoints(self):
      super()._setup_endpoints()
      self._app.register_blueprint(api.bp)
   ```
   - Implement the `check_status` method which returns a jsonified dictionary of status information
   ```python
   def check_status(self):
       pass
   ```
2. Implement your `app.py` this will need to create create the service, initialize it, and start it.
   Additionally you will need to setup two environment variables (preferably stored in `.flaskenv` or
   or a similar file):
   
   ```python
   from dotenv import load_dotenv
   from avista_portal.server import PortalServer
   from pathlib import Path
   import os
    
   path = Path(os.getcwd()) / ".flaskenv"
   if path.exists():
       load_dotenv(path)
    
   app = PortalServer.get_instance().app
       
   if __name__ == '__main__':
       PortalServer.get_instance().init()
       PortalServer.get_instance().start()
   ```

You can also see the complete documentation of the code on the
[documentation page](https://isu-avista.github.io/base-server/).

## Credits

This module was contributed to by:

- Isaac D. Griffith

## License

Copyright (c) 2020 Idaho State University Empirical Software Engineering Laboratory

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.