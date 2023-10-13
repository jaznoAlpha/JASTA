import requests
import os
import json
import time
import holidays

from datetime import datetime, timedelta
from typing import List, Optional

from z_classes import Stock_On_Watch_List
from x_method_for_returning_stock_watch_list import return_stock_watch_list

# Polygon.io API Key - Polygon.io is a free resource for getting historical price data for a particular stock
YOUR_API_KEY = "INSERT_API_KEY_HERE"

def polygon_day_by_day_data(stocks: List[Stock_On_Watch_List], start_date: datetime = None, end_date: datetime = None) -> List[dict]:
    """
    Fetches day-by-day data from Polygon for specific stocks and date range.

    Args:
        stocks (List[Stock_On_Watch_List]): List of stock objects containing the ticker symbols.
        start_date (datetime, optional): The start date for fetching the historical data.
            If not provided, today's date is used. (default is None)
        end_date (datetime, optional): The end date for fetching the historical data.
            If not provided, only one day worth of data is fetched. (default is None)

    Returns:
        List[dict]: The fetched historical data as a list of JSON objects.
    """

    # Set start_date as today's date if not provided
    if start_date is None:
        start_date = datetime.now().date()

    # Set end_date as start_date if it's not defined
    if end_date is None:
        end_date = start_date

    # Convert start_date and end_date to the desired format (e.g., 'YYYY-MM-DD')
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    result = []

    for stock in stocks:
        # Construct the API URL for fetching historical data
        url = f"https://api.polygon.io/v2/aggs/ticker/{stock.ticker}/range/1/day/{start_date_str}/{end_date_str}?apiKey={YOUR_API_KEY}"

        try:
            # Send a GET request to the API
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the JSON data from the response
                data = response.json()

                # Add the fetched data to the result array
                result.append(data)

            # Handle any other response status codes or errors
            else:
                print(f"Error: Request failed with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred during the request: {e}")

    # Return the array of JSON objects
    return result


def polygon_quarterly_data(stocks: List[Stock_On_Watch_List], start_quarter: str = None, start_year: int = None, end_quarter: str = None, end_year: int = None) -> List[dict]:
    """
    Fetches quarterly data from Polygon for a specific list of stocks and date range.

    Args:
        stocks (List[Stock_On_Watch_List]): The list of stock objects.

        start_quarter (str, optional): The start quarter in the format "Q1", "Q2", "Q3", "Q4".
        start_year (int, optional): The start year in the format YYYY.

        end_quarter (str, optional): The end quarter in the format "Q1", "Q2", "Q3", "Q4".
        end_year (int, optional): The end year in the format YYYY.

    Returns:
        List[dict]: The fetched quarterly data as a list of JSON objects.
    """

    # Get current date
    current_date = datetime.now().date()

    # Set default start date as the beginning of the current quarter if not provided
    if not start_quarter or not start_year:
        start_quarter, start_year = get_quarter_year(current_date)

    # Set default end date as today's date if not provided
    if not end_quarter or not end_year:
        end_quarter, end_year = get_quarter_year(current_date)

    # Convert start and end dates to datetime objects
    start_date = get_quarter_start_date(start_quarter, start_year)
    end_date = get_quarter_end_date(end_quarter, end_year)

    # Fetch day-by-day data for the stocks within the specified quarter range
    stock_data = polygon_day_by_day_data(stocks, start_date, end_date)
    print(end_date)

    return stock_data


def get_quarter_year(date: datetime):
    """
    Get the quarter and year for a given date.

    Args:
        date (datetime): The date for which to determine the quarter and year.

    Returns:
        (str, int): The quarter and year in the format (quarter, year).
    """
    quarter = (date.month - 1) // 3 + 1
    year = date.year
    return f"Q{quarter}", year


def get_quarter_start_date(quarter: str, year: int) -> datetime:
    """
    Get the start date of a given quarter and year.

    Args:
        quarter (str): The quarter in the format "Q1", "Q2", "Q3", "Q4".
        year (int): The year in the format YYYY.

    Returns:
        datetime: The start date of the quarter.
    """
    if quarter == "Q1":
        return datetime(year, 1, 1)
    elif quarter == "Q2":
        return datetime(year, 4, 1)
    elif quarter == "Q3":
        return datetime(year, 7, 1)
    elif quarter == "Q4":
        return datetime(year, 10, 1)
    else:
        raise ValueError("Invalid quarter.")


def get_quarter_end_date(quarter: str, year: int) -> datetime:
    """
    Get the end date of a given quarter and year.

    Args:
        quarter (str): The quarter in the format "Q1", "Q2", "Q3", "Q4".
        year (int): The year in the format YYYY.

    Returns:
        datetime: The end date of the quarter.
    """
    if quarter == "Q1":
        return datetime(year, 3, 31)
    elif quarter == "Q2":
        return datetime(year, 6, 30)
    elif quarter == "Q3":
        return datetime(year, 9, 30)
    elif quarter == "Q4":
        return datetime(year, 12, 31)
    else:
        raise ValueError("Invalid quarter.")

def polygon_save_quarterly_data(stocks: List[Stock_On_Watch_List], data, year: int, quarter: str):
    """
    Saves the quarterly data for each stock in a JSON file.

    Args:
        stocks (List[Stock_On_Watch_List]): List of stock objects.
        data: Quarterly data to be saved.
        year (int): The year of the data.
        quarter (str): The quarter of the data.

    Returns:
        None
    """

    # Set the base directory to store the data
    base_dir = r'C:\Users\Jason\Documents\0_JASTA\2_alpha\historical_data'

    # Iterate over each stock
    for stock in stocks:
        # Get the stock ticker
        ticker = stock.ticker

        # Create the directory path for the stock's quarterly data
        directory = os.path.join(base_dir, ticker, 'Quarterly_Data')
        os.makedirs(directory, exist_ok=True)

        # Generate the file name and file path
        file_name = f"{ticker}_{year}_{quarter}.json"
        file_path = os.path.join(directory, file_name)

        # Save the data as a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        # Print the success message with the file path
        print(f"Quarterly data for {ticker} saved as {file_path}.")

def polygon_update_all_quarterly_data() -> bool:
    """
    Updates the current quarter data for all stocks in the watch list for the current quarter and year.

    Returns:
        bool: True if we were able to update quarterly data for all stocks, False otherwise.
    """

    # Get the list of stocks from the watch list
    stocks = return_stock_watch_list()

    # Get today's date
    today = datetime.now().date()

    # Determine the current quarter and year based on today's date
    quarter = (today.month - 1) // 3 + 1
    year = today.year

    # Variable to track if the update is successful
    update_successful = True

    # Iterate over each stock
    for stock in stocks:
        # Fetch the quarterly data for the specified stock, current quarter, and year
        stock_data = polygon_quarterly_data(return_stock_watch_list(stock.ticker))

        # Check if the stock data is empty
        if not stock_data:
            print(f"Error: Q{quarter} data unavailable for {stock.ticker}")
            update_successful = False
            continue

        # Save the quarterly data as JSON files
        for data in stock_data:
            polygon_save_quarterly_data(return_stock_watch_list(stock.ticker), data, year, f"Q{quarter}")
            time.sleep(13)  # polygon.io only allows 5 calls per minute. This timer is to help comply with that.
    
    return update_successful

def polygon_minute_by_minute_data(stocks: List[Stock_On_Watch_List], start_date: datetime = None, end_date: datetime = None) -> List[dict]:
    """
    Fetches minute-by-minute data from Polygon for specific stocks and date range.

    Args:
        stocks (List[Stock_On_Watch_List]): List of stock objects containing the ticker symbols.
        start_date (datetime, optional): The start date for fetching the historical data.
            If not provided, today's date is used. (default is None)
        end_date (datetime, optional): The end date for fetching the historical data.
            If not provided, only one day's worth of data is fetched. (default is None)

    Returns:
        List[dict]: The fetched historical data as a list of JSON objects.
    """

    # Set start_date as today's date if not provided
    if start_date is None:
        start_date = datetime.now().date()

    # Set end_date as start_date if it's not defined
    if end_date is None:
        end_date = start_date

    # Convert start_date and end_date to the desired format (e.g., 'YYYY-MM-DD')
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    result = []

    for stock in stocks:
        # Construct the API URL for fetching historical data
        url = f"https://api.polygon.io/v2/aggs/ticker/{stock.ticker}/range/1/minute/{start_date_str}/{end_date_str}?apiKey={YOUR_API_KEY}"

        try:
            # Send a GET request to the API
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the JSON data from the response
                data = response.json()

                # Add the fetched data to the result array
                result.append(data)

            # Handle any other response status codes or errors
            else:
                print(f"Error: Request failed with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred during the request: {e}")

    # Return the array of JSON objects
    return result

def polygon_minute_daily_data(stocks: List[Stock_On_Watch_List], date: datetime = None) -> List[dict]:
    """
    Fetches daily data from Polygon for a specific list of stocks and date using minute-by-minute data.

    Args:
        stocks (List[Stock_On_Watch_List]): The list of stock objects.
        date (datetime, optional): The date for fetching the historical data.
            If not provided, today's date is used. (default is None)

    Returns:
        List[dict]: The fetched daily data as a list of JSON objects.
    """

    # Set date as today's date if not provided
    if date is None:
        date = datetime.now().date()

    # Fetch minute-by-minute data for the stocks on the specified date
    stock_data = polygon_minute_by_minute_data(stocks, date, date)
    print(date)

    return stock_data

def polygon_save_daily_minute_data(stocks: List[Stock_On_Watch_List], data, date: datetime):
    """
    Saves the daily minute data for each stock in a JSON file.

    Args:
        stocks (List[Stock_On_Watch_List]): List of stock objects.
        data: Daily minute data to be saved.
        date (datetime): The date of the data.

    Returns:
        None
    """

    # Set the base directory to store the data
    base_dir = r'C:\Users\Jason\Documents\0_JASTA\2_alpha\historical_data'

    # Iterate over each stock
    for stock in stocks:
        # Get the stock ticker
        ticker = stock.ticker

        # Create the directory path for the stock's minute data
        directory = os.path.join(base_dir, ticker, 'Minute_Data')
        os.makedirs(directory, exist_ok=True)

        # Generate the file name and file path
        file_name = f"{ticker}_{date.year}_{date.month:02d}_{date.day:02d}.json"
        file_path = os.path.join(directory, file_name)

        try:
            # Check if the file already exists
            if os.path.isfile(file_path):
                print(f"Overwriting existing file: {file_path}")
            else:
                print(f"Creating new file: {file_path}")

            # Save the data as a JSON file
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            # Print the success message with the file path
            print(f"Daily minute data for {ticker} saved as {file_path}.")

        except Exception as e:
            # Print the error message if an error occurred during file saving
            print(f"Error saving file {file_path}: {e}")

# def polygon_update_minute_data(stocks: Optional[List[Stock_On_Watch_List]] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> bool:
#     """
#     Updates the minute data for the specified stocks within the specified date range.

#     Args:
#         stocks (Optional[List[Stock_On_Watch_List]]): List of stock objects. If not provided, all stocks are considered.
#         start_date (Optional[datetime]): The start date for fetching the minute data. If not provided, only today's data is fetched.
#         end_date (Optional[datetime]): The end date for fetching the minute data. If not provided, end_date is set to start_date.

#     Returns:
#         bool: True if the minute data was successfully updated for all stocks, False otherwise.
#     """

#     # Get the list of stocks from the watch list if not provided
#     if stocks is None:
#         stocks = return_stock_watch_list()

#     # Get today's date if start_date is not provided
#     if start_date is None:
#         start_date = datetime.now().date()

#     # Set end_date as start_date if not provided
#     if end_date is None:
#         end_date = start_date

#     # Variable to track if the update is successful
#     update_successful = True

#     # Iterate over each stock
#     for stock in stocks:
#         # Fetch the minute data for each date within the specified date range
#         current_date = start_date
#         while current_date <= end_date:
#             stock_data = polygon_minute_by_minute_data(return_stock_watch_list(stock.ticker), current_date, current_date)
#             if stock_data:
#                 resultsCount = stock_data[0]['queryCount']

#             else:
#                 resultsCount = 0

#             time.sleep(13)

#             # Check if the stock data is empty
#             if not resultsCount:
#                 print(f"Error: No minute data available for {stock.ticker} on {current_date}")
#                 update_successful = False
#                 current_date += timedelta(days=1)
#                 continue

#             else:
#                 # Save the minute data as JSON files
#                 for data in stock_data:
#                     print(data['results'][0])
#                     timestamp_ms = data['results'][0]['t']
#                     timestamp_sec = timestamp_ms // 1000  # Convert milliseconds to seconds
#                     datetime_obj = datetime.fromtimestamp(timestamp_sec)
#                     polygon_save_daily_minute_data(return_stock_watch_list(stock.ticker), data, datetime_obj)

#             current_date += timedelta(days=1)

#     return update_successful

def polygon_update_minute_data(stocks: Optional[List[Stock_On_Watch_List]] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> bool:
    """
    Updates the minute data for the specified stocks within the specified date range.

    Args:
        stocks (Optional[List[Stock_On_Watch_List]]): List of stock objects. If not provided, all stocks are considered.
        start_date (Optional[datetime]): The start date for fetching the minute data. If not provided, only today's data is fetched.
        end_date (Optional[datetime]): The end date for fetching the minute data. If not provided, end_date is set to start_date.

    Returns:
        bool: True if the minute data was successfully updated for all stocks, False otherwise.
    """

    # Get the list of stocks from the watch list if not provided
    if stocks is None:
        stocks = return_stock_watch_list()

    # Get today's date if start_date is not provided
    if start_date is None:
        start_date = datetime.now().date()

    # Set end_date as start_date if not provided
    if end_date is None:
        end_date = start_date

    # Variable to track if the update is successful
    update_successful = True

    # Iterate over each stock
    for stock in stocks:
        # Fetch the minute data for each date within the specified date range
        current_date = start_date
        while current_date <= end_date:
            # Check if the current date is a weekend or a US holiday
            if current_date.weekday() >= 5 or current_date in holidays.US():
                print(f"Skipping weekend or holiday: {current_date}")
                current_date += timedelta(days=1)
                continue

            stock_data = polygon_minute_by_minute_data(return_stock_watch_list(stock.ticker), current_date, current_date)
            if stock_data:
                resultsCount = stock_data[0]['queryCount']
            else:
                resultsCount = 0

            time.sleep(13)

            # Check if the stock data is empty
            if not resultsCount:
                print(f"Error: No minute data available for {stock.ticker} on {current_date}")
                update_successful = False
                current_date += timedelta(days=1)
                continue
            else:
                # Save the minute data as JSON files
                for data in stock_data:
                    print(data['results'][0])
                    timestamp_ms = data['results'][0]['t']
                    timestamp_sec = timestamp_ms // 1000  # Convert milliseconds to seconds
                    datetime_obj = datetime.fromtimestamp(timestamp_sec)
                    polygon_save_daily_minute_data(return_stock_watch_list(stock.ticker), data, datetime_obj)

            current_date += timedelta(days=1)

    return update_successful
