import gspread
import os
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

jsonFile = open('credentials.json', 'r')
creds = json.load(jsonFile)
jsonFile.close()

creds['private_key_id'] = os.environ['PRIVATE_KEY_ID']
creds['private_key'] = os.environ['PRIVATE_KEY']

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
APPLICATION_NAME = 'CallScheduler'

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    creds,
    scopes=SCOPES
)
SPREADSHEET_NAME = 'CallSchedule'
# SPREADSHEET_NAME = 'CallScheduleDev'

gc = gspread.authorize(credentials)
spreadsheet = gc.open(SPREADSHEET_NAME)


class SpreadsheetReader():
    def getAvailableShifts():
        #gc = gspread.authorize(credentials)
        #spreadsheet = gc.open(SPREADSHEET_NAME)
        schedule = spreadsheet.worksheet('Schedule')
        df = pd.DataFrame(
            schedule.get_all_values()[1:],
            columns=schedule.get_all_values()[0:1][0])
        return df

    def getEmployees():
        #gc = gspread.authorize(credentials)
        #spreadsheet = gc.open(SPREADSHEET_NAME)
        employees = spreadsheet.worksheet('Employees')
        df = pd.DataFrame(
            employees.get_all_values()[1:],
            columns=employees.get_all_values()[0:1][0])
        return df

    def updateAvailableShiftsCell(row, column, value):
        #gc = gspread.authorize(credentials)
        #spreadsheet = gc.open(SPREADSHEET_NAME)
        schedule = spreadsheet.worksheet('Schedule')
        # why +2 here?? offset 1 for header, 1 for 0 idx
        schedule.update_cell(row+2, column, value)

    def updateEmployeesCell(row, column, value):
        #gc = gspread.authorize(credentials)
        #spreadsheet = gc.open(SPREADSHEET_NAME)
        employees = spreadsheet.worksheet('Employees')
        employees.update_cell(row+2, column, value)
