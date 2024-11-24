import unittest
from unittest.mock import patch, mock_open
from logcounter import (
    Validator,
    CookieCounter,
    PrintColor,
)


class TestValidator(unittest.TestCase):

    @patch("builtins.print")
    def test_validate_date_invalid_format(self, _):
        with self.assertRaises(SystemExit):
            Validator.validate_date("12-09-2018")

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_validate_file_not_found(self, mock_file, _):
        mock_file.side_effect = FileNotFoundError
        with self.assertRaises(SystemExit):
            Validator.validate_file("invalid_file.csv")

    @patch("builtins.open", new_callable=mock_open)
    def test_validate_file_success(self, mock_file):
        Validator.validate_file("valid_file.csv")
        mock_file.assert_called_once_with("valid_file.csv", "r", encoding="utf-8")


class TestCookieCounter(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+00:00
cookie1,2018-12-09T06:19:00+00:00
cookie2,2018-12-08T10:13:00+00:00
""",
    )
    def test_execute_count_cookies(self, _):
        counter = CookieCounter("dummy.csv")
        result = counter.execute("2018-12-09")
        self.assertEqual(result, ["cookie1"])  # cookie1 is the most active

    @patch("builtins.open", new_callable=mock_open, read_data="cookie,timestamp")
    def test_execute_no_cookies_when_file_is_empty(self, _):
        counter = CookieCounter("dummy.csv")
        result = counter.execute("2018-12-09")
        self.assertEqual(result, [])  # No cookies should return empty list

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+00:00
cookie1,2018-12-09T06:19:00+00:00
cookie2,2018-12-09T07:00:00+00:00
cookie3,2018-12-09T07:00:00+00:00
cookie3,2018-12-08T07:00:00+00:00
""",
    )
    def test_execute_no_cookies_for_wrong_date(self, _):
        counter = CookieCounter("dummy.csv")
        result = counter.execute("2012-12-09")
        self.assertEqual(
            result, []
        )  # No cookies at given time so should return empty list

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+00:00
cookie1,2018-12-09T06:19:00+00:00
cookie2,2018-12-09T07:00:00+00:00
cookie3,2018-12-09T07:00:00+00:00
cookie3,2018-12-08T07:00:00+00:00
""",
    )
    def test_execute_multiple_most_active_cookies(self, _):
        counter = CookieCounter("dummy.csv")
        result = counter.execute("2018-12-09")
        self.assertEqual(
            sorted(result), sorted(["cookie1", "cookie2"])
        )  # both should be returned

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+11:00
cookie1,2018-12-09T06:19:00+00:00
cookie2,2018-12-09T07:00:00+11:00
cookie3,2018-12-09T07:00:00+00:00
cookie3,2018-12-08T07:00:00+00:00
""",
    )
    def test_execute_respecting_timezone_in_calculations(self, _):
        counter = CookieCounter("dummy.csv")
        result = counter.execute("2018-12-09")
        self.assertEqual(
            sorted(result), sorted(["cookie1"])
        )  # Only cookie1 should be returned as cookie2 is in different timezone


class TestPrintColor(unittest.TestCase):

    @patch("builtins.print")
    def test_print_error(self, mock_print):
        PrintColor.print_error("Test error")
        mock_print.assert_called_once_with("\033[91mError:\033[0m Test error")


if __name__ == "__main__":
    unittest.main()
