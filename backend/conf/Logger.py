"""
    This file contains the logger which makes it easier to
    setup logging in all places of the project
"""
import logging

"""
    Default logger configuration
"""
FORMAT = "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"


class Logger:
    def __init__(self, name=__name__, level=logging.DEBUG, format=FORMAT):
        logging.basicConfig(format=format)
        self.log = logging.getLogger(name)
        self.log.setLevel(level=level)
