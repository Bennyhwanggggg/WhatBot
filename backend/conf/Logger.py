"""
    This file contains the logger which makes it easier to
    setup logging in all places of the project
"""
import logging

"""
    Default logger configuration
"""
FORMAT = "[%(asctime)s] %(levelname)s: %(name)s:\n%(message)s"


class Logger(logging.Logger):
    def __init__(self, name=__name__, level=logging.DEBUG, format=FORMAT):
        super().__init__(name)
        logging.basicConfig(format=format)
        self.log = logging.getLogger(name)
        self.log.setLevel(level=level)
