import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
import pandas as pd

from spreadsheet_reader import SpreadsheetReader

class TestSpreadsheetReader(unittest.TestCase):
    def setUp(self):
        print('Setup running')

    @patch('spreadsheet_reader.gspread.models.Worksheet')
    def test_get_available_shifts(self, mock_worksheet):
        sr = SpreadsheetReader('CallScheduleDev')
        shifts = [['Date', 'Day', 'Time', 'OnCall'],
                  ['1-Jul', 'Sunday', '0700-1530', 'Person1'],
                  ['2-Jul', 'Monday', '0000-0800', 'Person2']]

        sr.__create_credentials = MagicMock(return_value=None)
        sr.__open_spreadsheet = MagicMock(return_value=None)
        sr.spreadsheet.worksheet = MagicMock(return_value=mock_worksheet)
        mock_worksheet.get_all_values = MagicMock(return_value=shifts)

        df = sr.get_available_shifts()

        assert df.equals(pd.DataFrame(shifts[1:], columns=shifts[0]))

    @patch('spreadsheet_reader.gspread.models.Worksheet')
    def test_get_employees(self, mock_worksheet):
        sr = SpreadsheetReader('CallScheduleDev')
        employees = [['Name', 'NumShifts', 'Assigned', 'PhoneNumber', 'Current', 'GiveTo'],
                     ['Person1', '2', '2', '1234567890', 'FALSE', ''],
                     ['Person2', '2', '1', '1112223333', 'TRUE', 'Person1']]

        sr.__create_credentials = MagicMock(return_value=None)
        sr.__open_spreadsheet = MagicMock(return_value=None)
        sr.spreadsheet.worksheet = MagicMock(return_value=mock_worksheet)
        mock_worksheet.get_all_values = MagicMock(return_value=employees)

        df = sr.get_employees()

        assert df.equals(pd.DataFrame(employees[1:], columns=employees[0]))

    @patch('spreadsheet_reader.gspread.models.Worksheet')
    def test_update_available_shifts_cell(self, mock_worksheet):
        sr = SpreadsheetReader('CallScheduleDev')

        sr.__create_credentials = MagicMock(return_value=None)
        sr.__open_spreadsheet = MagicMock(return_value=None)
        sr.spreadsheet.worksheet = MagicMock(return_value=mock_worksheet)
        mock_worksheet.update_cell = MagicMock(return_value=None)

        sr.update_available_shifts_cell(1, 2, 3)
        mock_worksheet.update_cell.assert_called_with(3, 2, 3)

    @patch('spreadsheet_reader.gspread.models.Worksheet')
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
