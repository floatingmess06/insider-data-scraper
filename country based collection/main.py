import csv
from bs4 import BeautifulSoup
import requests
import time
import os


class Countries:
    """CONTAINS COUNTRIES INFOS"""

    AU = {"NAME": "AUSTRALIA", "URL": "https://www.insiderscreener.com/en/explore/au"}
    GM = {"NAME": "GERMANY", "URL": "https://www.insiderscreener.com/en/explore/de"}
    US = {"NAME": "USA", "URL": "https://www.insiderscreener.com/en/explore/us"}
    CA = {"NAME": "CANADA", "URL": "https://www.insiderscreener.com/en/explore/ca"}
    FR = {"NAME": "FRANCE", "URL": "https://www.insiderscreener.com/en/explore/fr"}
    SP = {"NAME": "SPAIN", "URL": "https://www.insiderscreener.com/en/explore/es"}
    IT = {"NAME": "ITALY", "URL": "https://www.insiderscreener.com/en/explore/it"}
    SZ = {"NAME": "SWITZERLAND", "URL": "https://www.insiderscreener.com/en/explore/ch"}
    BG = {"NAME": "BELGIUM", "URL": "https://www.insiderscreener.com/en/explore/be"}
    NH = {"NAME": "NETHERLANDS", "URL": "https://www.insiderscreener.com/en/explore/nl"}
    SW = {"NAME": "SWEDEN", "URL": "https://www.insiderscreener.com/en/explore/se"}
    GR = {"NAME": "GREECE", "URL": "https://www.insiderscreener.com/en/explore/gr"}
    IN = {"NAME": "INDIA", "URL": "https://www.insiderscreener.com/en/explore/in"}


def scrape_table(url: str):
    """Function to extract neccessary table's headers and rows

    Args:
        url (str): link of the page

    Returns:
        tuple(list): containing headers at 0th ind and rows at 1st
    """
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.select_one("div.table-responsive-md table")

    if table:
        headers = [th.text.strip() for th in table.select("thead th")]
        rows = []
        for row in table.select("tbody tr"):
            cells = [td.text.strip() for td in row.find_all(["td", "th"])]
            rows.append(cells)
        return headers, rows
    else:
        print(f"Table not found for URL: {url}")
        return None, None


def save_to_csv(filename, headers, rows):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    output_dir = "insider_data"
    os.makedirs(output_dir, exist_ok=True)

    for country_code, country_info in vars(Countries).items():
        if (
            isinstance(country_info, dict)
            and "NAME" in country_info
            and "URL" in country_info
        ):
            print(f"Scraping data for {country_info['NAME']}...")
            headers, rows = scrape_table(country_info["URL"])

            if headers and rows:
                filename = os.path.join(
                    output_dir, f"{country_info['NAME'].lower()}_insider_data.csv"
                )
                save_to_csv(filename, headers, rows)
                print(f"Data saved to {filename}")
            else:
                print(f"No data found for {country_info['NAME']}")

            # to avoid server restrictions
            time.sleep(2)

    print("Data extraction complete.")


if __name__ == "__main__":
    main()
