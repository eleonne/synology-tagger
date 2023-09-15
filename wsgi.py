#!/opt/conda/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
logging.error(sys.version)
sys.path.insert(0,"/app")

from web.api import app as application
application.secret_key = 'something super SUPER secret'
