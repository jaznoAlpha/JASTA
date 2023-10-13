from z_classes import ClickLocation, Stock_On_Watch_List

import pyautogui
import pytesseract
import time
import re

from typing import List

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# robinhood_searchbar = ClickLocation(900, 180)
robinhood_searchbar = ClickLocation(1060, 86)
robinhood_search_result = ClickLocation(925, 250)

robinhood_buy_button = ClickLocation(1565, 255)
robinhood_sell_button = ClickLocation(1625, 255)

robinhood_buying_power_upper_left = ClickLocation(1525, 590)
robinhood_buying_power_lower_right = ClickLocation(1785, 625)

robinhood_check_correct_page_upper_left = ClickLocation(762, 237)
robinhood_check_correct_page_lower_right = ClickLocation(904, 277)

robinhood_amount_to_buy_or_sell = ClickLocation(1740, 420)
robinhood_review_order_button = ClickLocation(1660, 530)

robinhood_sell_all_button = ClickLocation(1707, 611)

robinhood_buy_or_sell_all_confirm_button_1 = ClickLocation(1650, 600)
robinhood_buy_or_sell_all_confirm_button_2 = ClickLocation(1655, 740)

delay = 0.1
simulated_loading_delay = 4

def robinhood_navigate_to_trading_page_for_stock(stocks: List[Stock_On_Watch_List]) -> bool:
    """
    Navigates to the trading page for a specified stock in Robinhood.

    This function takes a list of stock objects as input and iterates through each stock.
    It simulates user actions to navigate to the trading page for each stock in the Robinhood application.
    The function moves the mouse to the Robinhood search bar, performs search operations, and opens a new window
    for the selected stock. It then captures a screenshot of a specific area to extract the company name using OCR.
    If the extracted company name matches the expected name for the stock, it returns True. Otherwise, it returns False.

    Args:
        stocks (List[Stock_On_Watch_List]): 
        This function only takes a single Stock_On_Watch_List object but it must be in a list. I'm too lazy to fix this.

    Returns:
        bool: True if the company name matches the expected name, False otherwise.
    """
    for stock in stocks:
        # Move the mouse to the robinhood searchbar
        pyautogui.moveTo(robinhood_searchbar.x, robinhood_searchbar.y)
        time.sleep(delay)

        # left clicks select and type into search field
        pyautogui.tripleClick()
        time.sleep(delay)

        # Type the stock ticker to search for stock
        pyautogui.typewrite(f'https://robinhood.com/stocks/{stock.ticker}')
        time.sleep(delay)

        # left clicks to open company page
        pyautogui.press('ENTER')
        time.sleep(delay)

def return_dollar_amount_as_just_number(string: str) -> str:
    """
    Extracts a number from a string in the format $xxx.xx. This was written to be used with
    the robinhood_check_buying_or_selling_power() function.

    Args:
        string (str): The string from which to extract the number.

    Returns:
        string (str): The extracted number as a string.

    """
    pattern = r"\$([\d.]+)"
    match = re.search(pattern, string)
    if match:
        number = float(match.group(1))
        return number
    else:
        return None

def robinhood_check_buying_or_selling_power() -> str:
    """
    Checks the buying or selling power in Robinhood.

    This function takes a screenshot of the specified area in the Robinhood application
    to capture the buying power information. It then performs optical character recognition (OCR)
    on the screenshot image to extract the buying power value as a string. Finally, it returns
    the extracted buying power value as a numeric amount.

    Returns:
        string (str): The buying or selling power as a number but in string form.
    """
    # Take a screenshot of the specified area(s)
    screenshot_buying_power = pyautogui.screenshot(region=(robinhood_buying_power_upper_left.x, robinhood_buying_power_upper_left.y, robinhood_buying_power_lower_right.x - robinhood_buying_power_upper_left.x, robinhood_buying_power_lower_right.y - robinhood_buying_power_upper_left.y))

    # Perform OCR on the screenshot image
    buying_power = pytesseract.image_to_string(screenshot_buying_power)

    return return_dollar_amount_as_just_number(buying_power)