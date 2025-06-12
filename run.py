from app import create_app, db
import logging
from logging.handlers import RotatingFileHandler
import os

app = create_app()

# Configure logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/incident_manager.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Incident Manager startup')

if __name__ == '__main__':
    app.run() 