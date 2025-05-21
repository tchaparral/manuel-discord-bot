'''
Logging configuration and utils module for Discord bot.
'''
import logging
import os
from datetime import datetime

# Directory where log files will be stored
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok = True)

# Create log filename with current date (format: bot_YYYY-MM-DD.log)
log_filename = os.path.join(LOG_DIR, f'bot_{datetime.now().strftime("%Y-%m-%d")}.log')

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler(log_filename, encoding = 'utf-8'),
    ]
)

def get_logger(name: str) -> logging.Logger:
    '''
    Create and configure a logger instance.
    '''
    return logging.getLogger(name)

def log_command(interaction, command_name: str, extra: str = ''):
    '''
    Logs the use of Dicord command in a standardized way
    '''
    logger = get_logger(__name__)
    user = interaction.user
    guild = interaction.guild.name if interaction.guild else 'DM'
    logger.info(f'[{guild}] {user.name} used /{command_name} {extra}')