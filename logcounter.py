import argparse
import sys
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo


class PrintColor:
    """Class to print colored text."""

    @staticmethod
    def print_error(message: str):
        """Print error message in red color."""
        ERR_COLOR = "\033[91m"
        ENDC = "\033[0m"
        print(f"{ERR_COLOR}Error:{ENDC} {message}")


class Validator:
    """Class to validate"""

    @staticmethod
    def validate_date(date: str, date_format: str = "%Y-%m-%d"):
        """Validate the date format."""

        try:
            datetime.strptime(date, date_format)
        except ValueError:
            Validator.__raise_error(
                "Invalid date format. Please use YYYY-MM-DD format."
            )

    @staticmethod
    def validate_file(filename: str):
        """Validate the file path."""

        try:
            with open(filename, "r", encoding="utf-8") as _:
                pass
        except FileNotFoundError:
            Validator.__raise_error("File not found. Please provide a valid file path.")

    @staticmethod
    def __raise_error(message: str):
        """Print error message and exit the program."""
        PrintColor.print_error(message)
        sys.exit(1)


class CookieCounter:
    """Class to count the number of cookies in a log file."""

    filename: str
    timezone: ZoneInfo
    _cookie_count: defaultdict

    def __init__(self, filename: str, timezone: ZoneInfo = ZoneInfo("UTC")):
        self.filename = filename
        self.timezone = timezone
        self._cookie_count = defaultdict(int)

    def execute(self, target_date: str) -> list[str]:
        """Execute the cookie counting process."""

        self._count_cookies_in_date(target_date)
        return self._retrieve_most_frequent_cookies()

    def _count_cookies_in_date(self, target_date: str):
        """Parse the cookie log file and count the cookies for the target date."""

        with open(self.filename, "r", encoding="utf-8") as file:
            next(file)  # Skip header
            for record in file:
                cookie, timestamp = record.strip().split(",")
                record_date = str(
                    datetime.fromisoformat(timestamp).astimezone(self.timezone).date()
                )
                if record_date == target_date:
                    self._cookie_count[cookie] += 1

    def _retrieve_most_frequent_cookies(self) -> list[str]:
        """Find the most active cookie(s) from the cookie count."""

        if not self._cookie_count:
            return []

        max_count = 0
        for cookie, count in self._cookie_count.items():
            if count > max_count:
                max_count = count
                most_active_cookies = [cookie]
            elif count == max_count:
                most_active_cookies.append(cookie)

        return most_active_cookies


def main():
    """Main function to parse the command line arguments and execute"""

    parser = argparse.ArgumentParser(
        description="Find the most active cookie for a specific day in UTC timezone."
    )
    parser.add_argument(
        "-f", "--file", required=True, help="Path to the cookie log file."
    )
    parser.add_argument(
        "-d", "--date", required=True, help="Date in YYYY-MM-DD format."
    )

    args = parser.parse_args()

    # validate input arguments
    Validator.validate_date(args.date)
    Validator.validate_file(args.file)

    # Get the most active cookie(s)
    most_active_cookies = CookieCounter(args.file).execute(args.date)

    for cookie in most_active_cookies:
        print(cookie)


if __name__ == "__main__":
    main()
