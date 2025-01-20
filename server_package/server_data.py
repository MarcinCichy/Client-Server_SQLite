import os
from datetime import datetime

"""
    Data for the Server part
"""

# ----------------------------------------------------

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024
ENCODE_FORMAT = "utf-8"


# # czy w chwili wprowadzenia SQL poniższe linijki kodu będą potrzebne?
# DB_FILES_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db_files')
# USERS_DATABASE = os.path.join(DB_FILES_DIRECTORY, 'users.json')
# MESSAGES_DATABASE = os.path.join(DB_FILES_DIRECTORY, 'messages.json')

# ----------------------------------------------------

CLOSE = "close"
MAX_MSG_IN_INBOX = 5

# ----------------------------------------------------

START_TIME = datetime.now()
DATE = datetime.now().strftime("%Y-%m-%d")
VERSION = "0.3.0"

# ----------------------------------------------------







