import logging

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add a stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

# Add a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(sh)
