import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
import pandas as pd

from cs.spreadsheet_reader import SpreadsheetReader
from cs.shift import Shift
from cs.employee import Employee

class TestSpreadsheetReader(unittest.TestCase):

    @patch('cs.spreadsheet_reader.gspread.models.Worksheet')
    def test_get_available_shifts_list(self, mock_worksheet):
        sr = SpreadsheetReader('CallScheduleDev')
        shifts = [['Date', 'Day', 'Time', 'OnCall'],
                  ['1-Jul', 'Sunday', '0700-1530', 'Person1'],
                  ['2-Jul', 'Monday', '0000-0800', 'Person2']]

        sr.__create_credentials = MagicMock(return_value=None)
        sr.__open_spreadsheet = MagicMock(return_value=None)
        sr.spreadsheet.worksheet = MagicMock(return_value=mock_worksheet)
        mock_worksheet.get_all_values = MagicMock(return_value=shifts)

        d = sr.get_available_shifts_list()
        s0 = Shift('1-Jul', 'Sunday', '0700-1530', 'Person1')
        s1 = Shift('2-Jul', 'Monday', '0000-0800', 'Person2')

        assert d[0] == s0
        assert d[1] == s1

    @patch('cs.spreadsheet_reader.gspread.models.Worksheet')
    def test_get_employees_list(self, mock_worksheet):
        sr = SpreadsheetReader('CallScheduleDev')
        employees = [['Name', 'NumShifts', 'Assigned', 'PhoneNumber', 'Current', 'GiveTo'],
                     ['Person1', '2', '2', '1234567890', 'FALSE', ''],
                     ['Person2', '2', '1', '1112223333', 'TRUE', 'Person1']]

        sr.__create_credentials = MagicMock(return_value=None)
        sr.__open_spreadsheet = MagicMock(return_value=None)
        sr.spreadsheet.worksheet = MagicMock(return_value=mock_worksheet)
        mock_worksheet.get_all_values = MagicMock(return_value=employees)

        d = sr.get_employees_list()
        e0 = Employee(0, 'Person1', 2, 2, '1234567890', 'FALSE', '')
        e1 = Employee(1, 'Person2', 2, 1, '1112223333', 'TRUE', 'Person1')

        assert d[0] == e0
        assert d[1] == e1

    @patch('cs.spreadsheet_reader.gspread.models.Worksheet')
    def test_update_available_shifts_cell(self, mock_worksheet):
        sr = SpreadsheetReader('CallScheduleDev')

        sr.__create_credentials = MagicMock(return_value=None)
        sr.__open_spreadsheet = MagicMock(return_value=None)
        sr.spreadsheet.worksheet = MagicMock(return_value=mock_worksheet)
        mock_worksheet.update_cell = MagicMock(return_value=None)

        sr.update_available_shifts_cell(1, 2, 3)
        mock_worksheet.update_cell.assert_called_with(3, 2, 3)

    @patch('cs.spreadsheet_reader.gspread.models.Worksheet')
    def test_update_employees_cell(self, mock_worksheet):
        sr = SpreadsheetReader('CallScheduleDev')

        sr.__create_credentials = MagicMock(return_value=None)
        sr.__open_spreadsheet = MagicMock(return_value=None)
        sr.spreadsheet.worksheet = MagicMock(return_value=mock_worksheet)
        mock_worksheet.update_cell = MagicMock(return_value=None)

        sr.update_employees_cell(1, 2, 3)
        mock_worksheet.update_cell.assert_called_with(3, 2, 3)

if __name__ == '__main__':
    unittest.main()
