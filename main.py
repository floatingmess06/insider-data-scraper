import os
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup


def submit_search_form(url, company_name, max_retries=3):
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    try:
        for attempt in range(max_retries):
            try:
                driver.get(url)
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "navbar_search_input"))
                )
                search_input.clear()
                search_input.send_keys(company_name)

                # Waiting for the dropdown to appear
                dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ui-menu"))
                )

                # Waiting for the first dropdown item to be clickable
                first_item = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".ui-menu .ui-menu-item")
                    )
                )

                # Click it
                first_item.click()

                # Wait for page load after click
                WebDriverWait(driver, 10).until(EC.url_changes(url))

                return driver.page_source
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(2)
                else:
                    print("Max retries reached. Unable to fetch data.")
                    return None
    finally:
        driver.quit()


def scrape_table_for_json(response):
    if not response:
        return None

    soup = BeautifulSoup(response, "html.parser")

    # Check for error messages
    error_msg = soup.select_one("div.alert.alert-danger")
    if error_msg:
        print(f"Error message found: {error_msg.text.strip()}")
        return None

    table = soup.select_one("div.table-responsive-md table")
    if table:
        headers = [th.text.strip() for th in table.select("thead th")]
        rows = []
        for row in table.select("tbody tr"):
            cells = [td.text.strip() for td in row.find_all(["td", "th"])]
            row_dict = {}
            for header, cell in zip(headers, cells):
                if header == "B/S\nTransaction type":
                    b_s, transaction_type = cell.split("\n", 1)
                    row_dict["B/S"] = b_s
                    row_dict["Transaction type"] = transaction_type
                elif header == "Insider and/or position":
                    insider_info = cell.split("\n")
                    row_dict["Insider"] = insider_info[0]
                    row_dict["Position"] = " ".join(insider_info[1:])
                elif header == "Nb. shares\nPrice\nValue":
                    nb_shares, price, value = cell.split("\n\n")
                    row_dict["Number of shares"] = nb_shares.split("\n")[0]
                    row_dict["Price"] = price
                    row_dict["Value"] = value
                elif header == "Details":
                    if cell:  # Only include Details if it's not empty
                        row_dict[header] = cell
                else:
                    row_dict[header] = cell
            rows.append(row_dict)
        return rows
    else:
        print("Table not found")
        return None


def scrape_table_for_csv(response):
    if not response:
        return None, None

    soup = BeautifulSoup(response, "html.parser")

    # Check for error messages
    error_msg = soup.select_one("div.alert.alert-danger")
    if error_msg:
        print(f"Error message found: {error_msg.text.strip()}")
        return None, None

    table = soup.select_one("div.table-responsive-md table")
    if table:
        headers = [th.text.strip() for th in table.select("thead th")]
        rows = []
        for row in table.select("tbody tr"):
            cells = [td.text.strip() for td in row.find_all(["td", "th"])]
            rows.append(cells)
        return headers, rows
    else:
        print("Table not found")
        return None, None


def save_to_csv(filename, headers, rows):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)


def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    url = "https://www.insiderscreener.com/en/"
    company_name = input("Enter the company name: ")
    output_dir = "insider_data"
    os.makedirs(output_dir, exist_ok=True)

    response = submit_search_form(url, company_name)
    if response:
        print("Response page received. Length:", len(response))
        print("Scraping data for selected company...")

        # uncomment if want to save data in csv
        # headers, rows = scrape_table(response)
        # if headers and rows:
        #     output_dir = os.path.join(output_dir, "csv")
        #     filename = os.path.join(
        #         output_dir,
        #         f"{company_name.replace(' ', '_').lower()}_insider_data.csv",
        #     )

        #     save_to_csv(filename, headers, rows)
        #     print(f"Data saved to {filename}")
        # else:
        #     print("No data found or unable to scrape the table.")

        data = scrape_table_for_json(response)

        if data:
            output_dir = os.path.join(output_dir, "json")
            filename = os.path.join(
                output_dir,
                f"{company_name.replace(' ', '_').lower()}_insider_data.json",
            )
            save_to_json(filename, data)
            print(f"Data saved to {filename}")
        else:
            print("No data found or unable to scrape the table.")
    else:
        print("Failed to retrieve the response page.")
