import logging.config
from colorlog import ColoredFormatter

def setup_logging():
    log_colors_config = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
    # Create a formatter with color support
    formatter = ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s',
        log_colors=log_colors_config
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    def setup_module_logger(name, level):
        logger = logging.getLogger(name)
        logger.setLevel(level)  
        return logger
    
    setup_module_logger('src.crawl', logging.DEBUG)
    setup_module_logger('src.index', logging.DEBUG)