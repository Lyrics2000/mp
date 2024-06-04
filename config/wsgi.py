
import os

from django.core.wsgi import get_wsgi_application
from logging.handlers import RotatingFileHandler


# Configure logging
import logging
log_file_path = 'app.log'  # Specify the path to your log file
logging.basicConfig(level=logging.DEBUG)




# Create a file handler
file_handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=2)  # Adjust maxBytes and backupCount as needed

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger().addHandler(file_handler)

logger = logging.getLogger(__name__)

logger.info("WSGI file is being executed.")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.settings')

application = get_wsgi_application()

