import os
import json

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class SpreadsheetReader:

    def __init__(self, spreadsheet_name):
        self.credentials = self.__create_credentials()
        self.spreadsheet_name = spreadsheet_name
        self.__open_spreadsheet()

    @staticmethod
    def __create_credentials():
        with open('credentials.json', 'r') as jc:
            creds = json.load(jc)
        creds['private_key_id'] = os.environ['PRIVATE_KEY_ID']
        creds['private_key'] = os.environ['PRIVATE_KEY']

        return ServiceAccountCredentials.from_json_keyfile_dict(
            creds,
            scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )

    def __open_spreadsheet(self):
        gc = gspread.authorize(self.credentials)
        self.spreadsheet = gc.open(self.spreadsheet_name)

    def __spreadsheet_to_df(self, sheet):
        schedule = self.spreadsheet.worksheet(sheet)
        return pd.DataFrame(
            schedule.get_all_values()[1:],
            columns=schedule.get_all_values()[0:1][0])

    def get_available_shifts(self):
        try:
            return self.__spreadsheet_to_df('Schedule')
        except Exception:
            self.__open_spreadsheet()
            return self.__spreadsheet_to_df('Schedule')

    def get_employees(self):
        try:
            return self.__spreadsheet_to_df('Employees')
        except Exception:
            self.__open_spreadsheet()
            return self.__spreadsheet_to_df('Employees')

    def update_available_shifts_cell(self, row, column, value):
        try:
            schedule = self.spreadsheet.worksheet('Schedule')
            # Offset 1 for header, 1 for 0 idx
            schedule.update_cell(row+2, column, value)
        except Exception:
            self.__open_spreadsheet()
            schedule = self.spreadsheet.worksheet('Schedule')
            # Offset 1 for header, 1 for 0 idx
            schedule.update_cell(row+2, column, value)

    def update_employees_cell(self, row, column, value):
        try:
            employees = self.spreadsheet.worksheet('Employees')
            # Offset 1 for header, 1 for 0 idx
            employees.update_cell(row+2, column, value)
        except Exception:
            self.__open_spreadsheet()
            employees = self.spreadsheet.worksheet('Employees')
            # Offset 1 for header, 1 for 0 idx
            employees.update_cell(row+2, column, value)
