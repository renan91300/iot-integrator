"""This project was generated with fastapi-mvc."""
import logging

from leds_cibele_api.wsgi import ApplicationLoader
from leds_cibele_api.version import __version__  # noqa: F401

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
