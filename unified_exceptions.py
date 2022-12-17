from flask import abort
from functools import wraps
import logging

class UnifiedExceptions:
    def __init__(self, filename):
        logging.basicConfig(level=logging.WARNING, filename=filename, format='[%(asctime)s] %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    
    def handle(self, func):
        @wraps(func)
        def function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error("Exception occurred", exc_info=True)
                #abort(500, description=e)
        return function
    
    def fatal(self, message):
        logging.fatal(message)

    def error(self, message):
        logging.error(message)

    def warning(self, message):
        logging.warning(message)

    def info(self, message):
        logging.info(message)

    def debug(self, message):
        logging.debug(message)

        