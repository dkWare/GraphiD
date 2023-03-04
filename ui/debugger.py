import logging
import colorlog

FORMAT = '%(log_color)s%(asctime)s [%(levelname)s] [%(module)s.%(classname)s.%(funcName)s:%(lineno)d] %(message)s'
FORMAT_FILE = '%(asctime)s [%(levelname)s] [%(module)s.%(classname)s.%(funcName)s:%(lineno)d] %(message)s'

class Tag:
    EVENTS = 0
    POSITION_CHANGE = 1
    VISUAL = 2
    LOGIC = 3

    MOUSE = 4
    KEYBOARD = 5

    FLAG_SETTINGS = 6
    VISUAL_SETTINGS = 7

    L_DEBUG = 9
    L_INFO = 10
    L_WARNING = 11
    L_ERROR = 12
    L_CRITICAL = 13

    M_UTILS = 14
    MU_VECTOR_HANDLING = 8

    M_MANAGE = 15
    M_FIELDS = 16

# Define the custom filter
class TagFilter(logging.Filter):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.instance = self
        self.filter_tags = []
        self.blocked_tags = []
        self._instance = self

    def filter(self, record):
        filter_tags = self.filter_tags
        blocked_tags = self.blocked_tags

        filter_out = True
        tag_available = hasattr(record, "tags")

        if tag_available:
            for tag in record.tags:
                if tag in blocked_tags:
                    return False

        if len(self.filter_tags) == 0:
            return True

        if tag_available:
            filter_out = not any(tag in record.tags for tag in self.filter_tags)

        return filter_out


# Create a logger and set the log level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define the colorlog formatter
formatter = colorlog.ColoredFormatter(
    FORMAT,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'light_green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

# Add the colorlog handler
handler = colorlog.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Add the tag filter to the handler
filter = TagFilter()
handler.addFilter(filter)  # add any tags you want to filter on here

# Add a file handler to the logger
file_handler = logging.FileHandler('test_data/log.txt')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(FORMAT_FILE))
logger.addHandler(file_handler)

# Test the logger
def test():
    logger.debug("Here is a normal Debug message", extra={'tags': ['my_tag']})
    logger.info("and a Info message", extra={'tags': ['my_tag']})

    logger.warning("!! Warning message !!", extra={})
    logger.error("Error message", extra={})
    logger.critical("Critical message", extra={})
