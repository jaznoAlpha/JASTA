from z_classes import Stock_On_Watch_List
from x_method_for_returning_stock_watch_list import return_stock_watch_list
from x_method_for_extracting_and_converting_polygon_data import polygon_save_daily_minute_data

from datetime import datetime, timedelta
from typing import List, Optional

import os
import json
import calendar

def return_file_path_quarterly_data(stock_ticker: str, target_date: Optional[datetime] = None) -> str:
    """
    Returns the file path for the quarterly data of a given stock ticker on a specific target date.

    Args:
        stock_ticker (str): The stock ticker symbol.
        target_date (datetime, optional): The target date for the quarterly data. Defaults to None.

    Returns:
        str: The file path of the quarterly data file. If the file is found, the path is returned.
             If the file is not found, an empty string is returned to indicate the absence of a valid path.
    """
    # Get the current date if target_date is not provided
    if target_date is None:
        target_date = datetime.now().date()

    # Determine the quarter of the target date
    quarter_of_target_date = f"Q{((target_date.month - 1) // 3) + 1}"

    # Construct the file path based on the stock ticker and target date quarter
    file_path = f"C:/Users/Jason/Documents/0_JASTA/2_alpha/historical_data/{stock_ticker}/Quarterly_Data/{stock_ticker}_{target_date.year}_{quarter_of_target_date}.json"
    
    # Check if the file exists at the specified path
    if os.path.exists(file_path):
        # Print success message if the file is found and returns the verified file path
        print(f"Success: File found for {stock_ticker} on {target_date}: {file_path}")
        return file_path
    else:
        # Print error message if the file is not found and returns an empty string to indicate this isn't a valid path
        print(f"Error: No file found for {stock_ticker} on {target_date}")
        return file_path

def return_file_path_minute_data(stock_ticker: str, target_date: Optional[datetime] = None) -> str:
    """
    Returns the file path for the minute data of a given stock ticker on a specific target date.

    Args:
        stock_ticker (str): The stock ticker symbol.
        target_date (datetime, optional): The target date for the minute data. Defaults to None.

    Returns:
        str: The file path of the quarterly data file. If the file is found, the path is returned.
             If the file is not found, an empty string is returned to indicate the absence of a valid path.
    """
    # Get the current date if target_date is not provided
    if target_date is None:
        target_date = datetime.now().date()

    # Format the target date as YYYY_MM_DD
    formatted_target_date = target_date.strftime("%Y_%m_%d")

    # Construct the file path based on the stock ticker and target date
    file_path = f"C:/Users/Jason/Documents/0_JASTA/2_alpha/historical_data/{stock_ticker}/Minute_Data/{stock_ticker}_{formatted_target_date}.json"
    
    # Check if the file exists at the specified path
    if os.path.exists(file_path):
        # Print success message if the file is found and returns the verified file path
        print(f"Success: File found for {stock_ticker} on {target_date}: {file_path}")
        return file_path
    else:
        # Print error message if the file is not found and returns an empty string to indicate this isn't a valid path
        print(f"Error: No file found for {stock_ticker} on {target_date}")
        return ""
    
def read_json_from_file(file_path: str) -> dict:
    """
    Reads and returns the JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        print(f"Success: Was able to find and read .json file at path: {file_path}")
        return json_data
    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {file_path}")
        return {}
    
def return_data_from_quarterly_data_json(stocks: Optional[List[Stock_On_Watch_List]] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[dict]:
    """
    Returns just the results from the JSON file and skips the useless entries from the JSON.

    Args:
        stocks (Optional[List[Stock_On_Watch_List]]): List of stock objects. Defaults to None.
        start_date (Optional[datetime]): The start date for fetching the data. Defaults to None.
        end_date (Optional[datetime]): The end date for fetching the data. Defaults to None.

    Returns:
        List[dict]: A list of dictionaries containing the results from the JSON file for each stock.
                    Each dictionary has two properties: 'ticker' (assigned with stock.ticker) and 'data' (equal to quarter_data_results[0]).
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

    current_date = start_date
    result = []  # Initialize an empty list to store the results

    while current_date <= end_date:
        # Perform operations for the current date

        for stock in stocks:
            quarterly_data = read_json_from_file(return_file_path_quarterly_data(stock.ticker, current_date))
            quarterly_data_results = quarterly_data.get('data') or quarterly_data.get('results')

            if quarterly_data_results is not None:
                result.append({
                    'ticker': stock.ticker,
                    'data': quarterly_data_results
                })  # Add the dictionary to the main result list
            else:
                print(f'There was no data from {stock.name} on {current_date}')
                result.append({
                    'ticker': stock.ticker,
                    'data': []
                })  # Add the object to the main result list but with an empty array so that it's obvious there's no data

        # Increment the month by 3
        month = current_date.month + 3
        year = current_date.year + month // 12
        month = month % 12 or 12  # Adjust month to be within 1 to 12

        # Find the last valid day of the month
        last_day = calendar.monthrange(year, month)[1]

        # Set the day to the minimum value between the current day and the last valid day
        day = min(current_date.day, last_day)

        # Create a new datetime object with the updated year, month, and day
        current_date = current_date.replace(year=year, month=month, day=day)

    return result  # Return the finished list of dictionaries with 'ticker' and 'data' properties

def return_data_from_minute_data_json(stocks: Optional[List[Stock_On_Watch_List]] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[dict]:
    """
    Returns just the results from the JSON file and skips the useless entries from the JSON.

    Args:
        stocks (Optional[List[Stock_On_Watch_List]]): List of stock objects. Defaults to None.
        start_date (Optional[datetime]): The start date for fetching the data. Defaults to None.
        end_date (Optional[datetime]): The end date for fetching the data. Defaults to None.

    Returns:
        List[dict]: A list of dictionaries containing the results from the JSON file for each stock.
                    Each dictionary has two properties: 'ticker' (assigned with stock.ticker) and 'data' (equal to minute_data_results).
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

    current_date = start_date
    result = []  # Initialize an empty list to store the results

    while current_date <= end_date:
        # Perform operations for the current date

        for stock in stocks:
            minute_data = read_json_from_file(return_file_path_minute_data(stock.ticker, current_date))
            minute_data_results = minute_data.get('data') or minute_data.get('results')

            if minute_data_results is not None:
                result.append({
                    'ticker': stock.ticker,
                    'data': minute_data_results
                })  # Add the dictionary to the main result list
            else:
                print(f'There was no data from {stock.name} on {current_date}')
                result.append({
                    'ticker': stock.ticker,
                    'data': []
                })  # Add the object to the main result list but with an empty array so that it's obvious there's no data

        # Increment the current_date by one day
        current_date += timedelta(days=1)

    return result  # Return the finished list of dictionaries with 'ticker' and 'data' properties

def verify_historical_data_files(stocks: Optional[List[Stock_On_Watch_List]] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[dict]:
    """
    This function identifies and finds any missing files.

    Args:
        stocks (Optional[List[Stock_On_Watch_List]]): List of stock objects. Defaults to None.
        start_date (Optional[datetime]): The start date for fetching the data. Defaults to None.
        end_date (Optional[datetime]): The end date for fetching the data. Defaults to None.

    Returns:
        List[dict]: A list of dictionaries containing the results from the JSON file for each stock.
                    Each dictionary has two properties: 'ticker' (assigned with stock.ticker) and 'data' (equal to minute_data_results).
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

    date_to_be_analyzed = start_date
    missing_dates = []

    while date_to_be_analyzed <= end_date:
        for stock in stocks:
            min_data = return_data_from_minute_data_json(return_stock_watch_list(stock.ticker), date_to_be_analyzed)[0]['data']
            qtl_data = return_data_from_quarterly_data_json(return_stock_watch_list(stock.ticker), date_to_be_analyzed)[0]['data']

            qtl_dates = set()
            min_date = None

            # Extract date information from quarterly data
            for entry in qtl_data:
                qtl_data_milliseconds = entry['t']
                qtl_data_seconds = qtl_data_milliseconds / 1000
                qtl_data_delta = timedelta(seconds=qtl_data_seconds)
                qtl_data_date_temp = datetime(1970, 1, 1) + qtl_data_delta
                qtl_data_date = qtl_data_date_temp.replace(second=0, microsecond=0, minute=0, hour=0)
                # qtl_dates.add(qtl_data_date)
                if(qtl_data_date == date_to_be_analyzed):
                    qtl_dates.add(qtl_data_date)
                

            # Extract date information from minute data (only first entry)
            if min_data:
                min_data_milliseconds = min_data[0]['t']
                min_data_seconds = min_data_milliseconds / 1000
                min_data_delta = timedelta(seconds=min_data_seconds)
                min_data_date_temp = datetime(1970, 1, 1) + min_data_delta
                min_date = min_data_date_temp.replace(second=0, microsecond=0, minute=0, hour=0)
                if not qtl_dates:
                    missing_dates.append({
                    'ticker': stock.ticker,
                    'missing': 'qtl_data',
                    'date': date_to_be_analyzed
                })  # Add the dictionary to the main result list

            elif not min_data:
                if(qtl_dates):
                    missing_dates.append({
                    'ticker': stock.ticker,
                    'missing': 'min_data',
                    'date': date_to_be_analyzed
                })  # Add the dictionary to the main result list

        # Increment the date by one day
        date_to_be_analyzed += timedelta(days=1)
    
    print(missing_dates)