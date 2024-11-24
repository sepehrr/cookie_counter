# Cookie Counter

A simple Python application to find the most active cookies from a log file for a specific day in UTC timezone.

## Features

- Parses cookie log files.
- Counts occurrences of each cookie for a specified date.
- Returns the most frequent cookie(s) for that date.

## Requirements

- Python 3.7 or higher
- Any additional dependencies (if any, e.g., `zoneinfo` for timezone functionality)

## Structure

```simple
your_project/
│
├── logcounter.py          # Main application code
├── cookie_log.csv         # Sample cookie log file
└── test_logcounter.py     # Test code for the application
└── README.md              # Project documentation
```

## Getting Started

### Prerequisites

Before you begin, ensure you have Python installed on your machine. You can check if Python is installed by running:

```bash
python --version
```

If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

### Installation

1. Download the project source code or get them from the repository:

   ```bash
   git clone <repository-url>
   ```

2. Change into the project directory:

   ```bash
   cd <project-directory>
   ```

3. (Optional) Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

### Usage

To run the cookie counter application, use the following command:

```bash
python logcounter.py -f <path_to_cookie_log_file> -d <YYYY-MM-DD>
```

#### Example

```bash
python logcounter.py -f cookie_log.csv -d 2018-12-09
```

This command will output the most active cookie(s) for the specified date (e.g., December 9, 2018).

### Running Tests

To ensure the application is functioning as expected, you can run the test suite provided:

```bash
python3 -m unittest test_logcounter.py
```

To run a specific test case, use:

```bash
python -m unittest test_logcounter.TestValidator.test_validate_date_invalid_format
```

### Input Format

The input CSV log file should be structured as follows:

```csv
cookie,timestamp
cookie_name_1,2023-10-01T12:34:56+00:00
cookie_name_2,2023-10-01T09:21:00+00:00
...
```

- The first line is a header.
- Subsequent lines contain cookies and their respective timestamps.

## Acknowledgments

- [Python](https://www.python.org) for the programming language.
- [unittest](https://docs.python.org/3/library/unittest.html) for the testing framework.
