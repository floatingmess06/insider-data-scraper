# Insider Data Scraper

This tool scrapes insider trading data from insiderscreener.com for a company and saves the data into separate JSON/CSV files.

## Features

- Scrapes insider trading data for demanded company
- Saves data in a separate JSON/CSV file
- Handles network requests responsibly with delays between requests
- Uses custom User-Agent to mimic browser behavior

## Requirements

- Python 3.12

## Installation

1. Install Python

Ensure you have Python installed on your system. You can download and install the latest version of Python from python.org.

2. Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment is a good practice to manage project-specific dependencies.

```
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
```

3. Install Required Python Packages

```
pip install -r requirements.txt
```

## Usage

1. Run the script:

```
python main.py
```

You will be prompted to enter the company name. The script will then perform the web scraping and save the data to a JSON/CSV file.

2. The script will create an "insider_data" directory in the same location as the script.
3. JSON/CSV file for each company will be saved in the "insider_data" directory.

## Additional Considerations

- Firefox Installation: Ensure you have Firefox installed on your system since the script uses Firefox for web scraping.
- Adjust Timeouts: If you experience timeouts or other timing issues, consider adjusting the WebDriverWait durations in the script.
- Error Handling: The script includes basic error handling. Depending on the website's behavior, you might need to enhance this further.

## Notes

- This tool is for educational purposes only.
- Be sure to comply with insiderscreener.com's terms of service and robots.txt file.
- The website's structure may change over time, which could require updates to the scraping logic.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/floatingmess06/insider-data-scraper/issues) if you want to contribute.


