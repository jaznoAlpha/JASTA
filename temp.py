from x_method_for_extracting_and_converting_yahoo_data import extract_historical_data_from_yahoo
from x_method_for_extracting_and_converting_polygon_data import polygon_day_by_day_data, polygon_quarterly_data, polygon_update_all_quarterly_data, polygon_update_minute_data
from x_method_for_handling_robinhood import robinhood_navigate_to_trading_page_for_stock, robinhood_check_buying_or_selling_power
from x_methods_for_starting_up import startup_setup_windows
from x_method_for_handling_ibka import return_current_price_of_stock
from x_method_for_handling_stock_purchase_decision import decide_what_to_do_about_current_price
from x_method_for_handling_what_happens_after_analysis import method_for_handling_what_happens_after_analysis

from x_method_for_returning_stock_watch_list import return_stock_watch_list

from z_classes import Stock_On_Watch_List, MilTime

import pytesseract
import time

from datetime import timedelta
import datetime
import os

# # Define the file name variable
ticker = "TSLA"  # Replace with the desired ticker symbol
year = 2023
quarter = 'Q1'

focused_stock_list = return_stock_watch_list(ticker)
focused_stock = focused_stock_list[0]
current_price_of_focused_stock = return_current_price_of_stock(focused_stock_list)

# Get today's date
# today = datetime.now().date()

# # Calculate yesterday's date
# yesterday = today - timedelta(days=1)

# Fetch day-by-day data for the stocks
# for stock in return_stock_watch_list():
#     while True:
#         time.sleep(3)
#         result = robinhood_navigate_to_trading_page_for_stock(return_stock_watch_list(stock.ticker))
#         if result:
#             print(f"Success: Successfully navigated to trading page for {stock.ticker}")
#             break
#         else:
#             print(f"Failure: Failed to navigate to trading page for {stock.ticker}. Retrying...")

# if(startup_setup_windows()):
#     print("successfully pulled up windows!")

# else:
#     print("Failed setting up windows!")

# robinhood_navigate_to_trading_page_for_stock(return_stock_watch_list(ticker))

# method_for_handling_what_happens_after_analysis()
# startup_setup_windows()
print(current_price_of_focused_stock)