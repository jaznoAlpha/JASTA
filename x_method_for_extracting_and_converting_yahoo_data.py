from z_classes import ClickLocation
from x_method_for_returning_stock_watch_list import return_stock_watch_list

import pyautogui
import time
import csv
import json
import os
import clipboard
from datetime import datetime

"""
All of the following functions assume yahoo finance is already open, half screened on the right, 
and already on stock trading page like AAPL. 

Here's a link: https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch

You also need to make sure the downloads folder is completely clear! Or this won't
work right!
"""

def convert_yahoo_data(file_name, json_file_name, start_date, end_date):
    # Specify the base directory
    base_directory = r'C:\Users\Jason\Documents\0_JASTA\2_alpha\historical_data'

    # Create the directory path
    directory_path = os.path.join(base_directory, file_name, 'Quarterly_Data')

    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    # Specify the Downloads folder path
    downloads_folder = os.path.expanduser("~/Downloads")

    # Construct the file path
    file_path = os.path.join(downloads_folder, f"{file_name}.csv")
    json_file_path = os.path.join(directory_path, f"{json_file_name}.json")

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file and read the data
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            # Filter the data based on start and end dates
            filtered_data = []
            for row in reader:
                date = row['Date']
                if start_date <= date <= end_date:
                    filtered_row = {
                        "v": float(row["Volume"]),
                        "vw": float(row["Adj Close"]),
                        "o": float(row["Open"]),
                        "c": float(row["Close"]),
                        "h": float(row["High"]),
                        "l": float(row["Low"]),
                        "t": int(datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000),
                        "n": 0
                    }
                    filtered_data.append(filtered_row)

            # Construct the JSON object
            json_data = {
                'ticker': file_name,
                'queryCount': len(filtered_data),
                'resultsCount': len(filtered_data),
                'data': filtered_data,
                'status': 'DELAYED',
                'request_id': '',
                'count': len(filtered_data)
            }

            # Write the JSON data to a file
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)

            print(f"Filtered data saved to '{json_file_path}'.")
            return True
    else:
        print(f"File '{file_name}.csv' not found in the Downloads folder.")
        return False

def download_csv_from_yahoo (stock, start_year, end_year):
    # If an action needs a delay, it will use this delay.
    delay = 0.1
    loading_delay = 4

    ticker_name = stock.ticker

    init_month = '01'
    init_day = '01'
    init_year = str(start_year)

    final_month = '12'
    final_day = '31'
    final_year = str(end_year)

    # Define the target coordinates for clicking
    location_searchbar = ClickLocation(1675, 210)
    location_historical_data_button = ClickLocation(1985, 660)
    location_time_period_button = ClickLocation(1570, 785)
    location_start_date_changer = ClickLocation(1460, 950)
    location_end_date_changer = ClickLocation(1540, 1005)
    location_date_done_button = ClickLocation(1490, 1075)
    location_date_apply_button = ClickLocation(2015, 830)
    location_download_button = ClickLocation(2055, 895)
    location_div_check = ClickLocation(1400, 615)

    #add a slight delay after start
    time.sleep(delay)

    # Move the mouse to searchbar in yahoo finance's website
    pyautogui.moveTo(location_searchbar.x, location_searchbar.y)
    time.sleep(delay)

    # clicks inside searchbar to begin search and waits for loading time
    pyautogui.leftClick()
    time.sleep(delay)

    # Types the ticker name into the searchbar bringing up the stock
    pyautogui.typewrite(stock.yahooURL)
    time.sleep(delay)

    # Press the Enter key
    pyautogui.press('enter')
    time.sleep(loading_delay)

    # Move the mouse to where there might a dividend alert
    pyautogui.moveTo(location_div_check.x, location_div_check.y)
    time.sleep(delay)

    # double clicks the dividend text if its there
    pyautogui.doubleClick()
    time.sleep(delay)

     # copies the text to check it
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(delay)

    # Get the string contents from the clipboard
    dividend_check = clipboard.paste()

    # Check if the string is equal to "Dividend"
    if dividend_check == "Dividend":
        print("This page reported that the company in question issued a dividend'")
    else:
        print("This page reported that the company in question did not issue a dividend'")

        location_time_period_button = ClickLocation(1570, 745)
        location_start_date_changer = ClickLocation(1460, 910)
        location_end_date_changer = ClickLocation(1540, 965)
        location_date_done_button = ClickLocation(1490, 1035)
        location_date_apply_button = ClickLocation(2015, 790)
        location_download_button = ClickLocation(2055, 855)

    # Clear the clipboard for the next round
    clipboard.copy('')

    # Move the mouse to the historical data button in yahoo finance's website
    pyautogui.moveTo(location_historical_data_button.x, location_historical_data_button.y)
    time.sleep(delay)

    # clicks the button to access historical data
    pyautogui.leftClick()
    time.sleep(loading_delay)

    # Move the mouse to the time period button in yahoo finance's website
    pyautogui.moveTo(location_time_period_button.x, location_time_period_button.y)
    time.sleep(delay)

    # clicks the button to access date changer popup
    pyautogui.leftClick()
    time.sleep(delay)

    # Move the mouse to the start date field in the date changer popup
    pyautogui.moveTo(location_start_date_changer.x, location_start_date_changer.y)
    time.sleep(delay)

    # clicks the button to access the start date field
    pyautogui.leftClick()
    time.sleep(delay)

    # Types the initial month into the start date field
    pyautogui.typewrite(init_month)
    time.sleep(delay)

    # Types the initial day into the start date field
    pyautogui.typewrite(init_day)
    time.sleep(delay)

    # Types the initial year (2017) into the start date field
    pyautogui.typewrite(init_year)
    time.sleep(delay)

    # Move the mouse to the end date field in the date changer popup
    pyautogui.moveTo(location_end_date_changer.x, location_end_date_changer.y)
    time.sleep(delay)

    # clicks the button to access the end date field
    pyautogui.leftClick()
    time.sleep(delay)

    # Types the final month into the end date field
    pyautogui.typewrite(final_month)
    time.sleep(delay)

    # Types the final day into the end date field
    pyautogui.typewrite(final_day)
    time.sleep(delay)

    # Types the final year (2022) into the end date field
    pyautogui.typewrite(final_year)
    time.sleep(delay)

    # Move the mouse to the done button to effectively change the dates
    pyautogui.moveTo(location_date_done_button.x, location_date_done_button.y)
    time.sleep(delay)

    # clicks the button to change the dates
    pyautogui.leftClick()
    time.sleep(delay)

    # Move the mouse to the apply button to effectively change the dates
    pyautogui.moveTo(location_date_apply_button.x, location_date_apply_button.y)
    time.sleep(delay)

    # clicks the apply to change the dates
    pyautogui.leftClick()
    time.sleep(loading_delay)

    # Move the mouse to the download button
    pyautogui.moveTo(location_download_button.x, location_download_button.y)
    time.sleep(delay)

    # should download the csv file
    pyautogui.leftClick()
    time.sleep(loading_delay)

    # Specify the file extension
    file_extension = ".csv"

    # Construct the complete file name
    complete_file_name = ticker_name + file_extension

    # Specify the Downloads folder path
    downloads_folder = os.path.expanduser("~/Downloads")

    # Construct the file path
    file_path = os.path.join(downloads_folder, complete_file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        print(f"File '{ticker_name}'.csv was downloaded successfully.")
        return True
    else:
        print(f"File '{ticker_name}'.csv failed to download.")
        return False
    

def extract_historical_data_from_yahoo(ticker=None, start_year=2017, end_year=2022):
    """
    Extracts historical data for the given ticker(s) from Yahoo Finance and the converts it to a standardized JSON

    Args:
        ticker (str or list, optional): Ticker(s) to extract historical data for.
            If not provided, historical data for all tickers will be extracted.
            Defaults to None.

    Returns:
        None

    """
    # Retrieve the stock watch list
    if ticker is None:
        stock_list = return_stock_watch_list()
    elif isinstance(ticker, str):
        stock_list = return_stock_watch_list(ticker)
    elif isinstance(ticker, list):
        stock_list = return_stock_watch_list(*ticker)
    else:
        print("Invalid ticker format. Please provide a string or a list of strings.")
        return

    # Define the start and end dates for each quarter
    quarters = [("Q1", "01-01", "03-31"),
                ("Q2", "04-01", "06-30"),
                ("Q3", "07-01", "09-30"),
                ("Q4", "10-01", "12-31")]
    start_quarter = 1
    end_quarter = 4

    # Process each stock in the stock watch list
    for stock in stock_list:
        # Extract historical data for the stock
        if download_csv_from_yahoo(stock, start_year, end_year):
            # Process each quarter for the specified years
            for year in range(start_year, end_year + 1):
                if year == start_year:
                    start_quarter = start_quarter
                else:
                    start_quarter = 1

                if year == end_year:
                    end_quarter = end_quarter
                else:
                    end_quarter = 4

                for quarter in range(start_quarter, end_quarter + 1):
                    print(f"Processing year: {year}")
                    print(f"Processing quarter: {quarter}")
                    json_file_name = f"{stock.ticker}_{year}_Q{quarter}"
                    json_start_date = f"{year}-{quarters[quarter-1][1]}"
                    json_end_date = f"{year}-{quarters[quarter-1][2]}"

                    # Process the downloaded file and save filtered data as JSON
                    if not convert_yahoo_data(stock.ticker, json_file_name, json_start_date, json_end_date):
                        print(f"Error occurred while converting data for ticker '{stock.ticker}' "
                              f"and period '{json_file_name}'.")
                        break
        else:
            print(f"Failed to download CSV file for ticker '{stock.ticker}'.")
            break