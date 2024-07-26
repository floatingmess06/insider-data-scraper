# Insider Data Scraper

This tool scrapes insider trading data from insiderscreener.com for multiple countries and saves the data into separate CSV files.

## Features

- Scrapes insider trading data for 13 countries
- Saves data for each country in a separate CSV file
- Handles network requests responsibly with delays between requests
- Uses custom User-Agent to mimic browser behavior

## Requirements

- Python 3.10

## Installation

1. Clone this repository or download the script.
2. Install the required Python packages:

```
pip install beautifulsoup4 requests
```

## Usage

1. Run the script:

```
python main.py
```

2. The script will create an "insider_data" directory in the same location as the script.
3. CSV files for each country will be saved in the "insider_data" directory.

## Supported Countries

- Australia
- Germany
- USA
- Canada
- France
- Spain
- Italy
- Switzerland
- Belgium
- Netherlands
- Sweden
- Greece
- India

## Notes

- This tool is for educational purposes only.
- Be sure to comply with insiderscreener.com's terms of service and robots.txt file.
- The website's structure may change over time, which could require updates to the scraping logic.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/insider-data-scraper/issues) if you want to contribute.


