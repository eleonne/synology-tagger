#!/opt/conda/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/app/web/")

from web.api import app as application
application.secret_key = 'something super SUPER secret'
