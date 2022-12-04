import logging

class UnifiedExceptions:
    def __init__(self, filename):
        logging.basicConfig(level=logging.DEBUG, filename=filename, format='[%(asctime)s] %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    
    def handle(self, func):
        def function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error("Exception occurred", exc_info=True)
        return function