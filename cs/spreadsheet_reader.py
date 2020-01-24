import os
import json

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from .employee import Employee
from .shift import Shift


class SpreadsheetReader:
    SHIFTS_NAME = 4

    ASSIGNED = 3
    CURRENT = 5
    GIVE_TO = 6

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
            scopes='https://www.googleapis.com/auth/spreadsheets'
        )

    def __open_spreadsheet(self):
        print('SPREADSHEET_NAME = {}'.format(self.spreadsheet_name))
        gc = gspread.authorize(self.credentials)
        self.spreadsheet = gc.open(self.spreadsheet_name)

    @staticmethod
    def __shifts_spreadsheet_to_list(ws):
        return [Shift(v[0], v[1], v[2], v[3]) for v in ws.get_all_values()[1:]]

    @staticmethod
    def __employees_spreadsheet_to_list(ws):
        return [Employee(k, v[0], int(v[1]), int(v[2]), v[3], v[4], v[5])
                for k, v in enumerate(ws.get_all_values()[1:])]

    def get_available_shifts_list(self):
        sheet = 'Schedule'
        try:
            ws = self.spreadsheet.worksheet(sheet)
        except Exception:
            self.__open_spreadsheet()
            ws = self.spreadsheet.worksheet(sheet)
        return self.__shifts_spreadsheet_to_list(ws)

    def get_employees_list(self):
        sheet = 'Employees'
        try:
            ws = self.spreadsheet.worksheet(sheet)
        except Exception:
            self.__open_spreadsheet()
            ws = self.spreadsheet.worksheet(sheet)
        return self.__employees_spreadsheet_to_list(ws)

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

    def update_employees_assigned(self, row, value):
        self.update_employees_cell(row, SpreadsheetReader.ASSIGNED, value)

    def update_employees_current(self, row, value):
        self.update_employees_cell(row, SpreadsheetReader.CURRENT, value)

    def update_employees_give_to(self, row, value):
        self.update_employees_cell(row, SpreadsheetReader.GIVE_TO, value)

    def assign_shift(self, employee):
        self.update_employees_assigned(employee.seniority, employee.assigned_shifts)
        self.update_employees_current(employee.seniority, employee.current)
        self.update_employees_give_to(employee.seniority, employee.give_to)

    def add_name_to_shift(self, idx, shift):
        self.update_available_shifts_cell(idx, SpreadsheetReader.SHIFTS_NAME, shift.on_call)
