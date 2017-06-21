import logging

try:
    from config import LOG_LEVEL
except:
    LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)