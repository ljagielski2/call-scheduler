import configparser
import os

from flask import Flask

from cs.spreadsheet_reader import SpreadsheetReader

APP = Flask(__name__)

CONFIG = configparser.ConfigParser()
CONFIG.read('application.ini')
CONFIG = CONFIG[os.environ['APP_ENV']]

SPREADSHEET = SpreadsheetReader(CONFIG['SPREADSHEET_NAME'])


from cs.contact_scheduler import ContactScheduler
SCHEDULER = ContactScheduler()

from cs import views
