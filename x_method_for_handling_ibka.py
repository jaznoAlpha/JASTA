from z_classes import Stock_On_Watch_List
from x_method_for_returning_stock_watch_list import return_stock_watch_list

import pyautogui
import pytesseract

from typing import List

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def return_current_price_of_stock(stocks: List[Stock_On_Watch_List]) -> str:
    """
    Returns the current price of the first stock in the provided list as a string.

    Parameters:
    - stocks (List[Stock_On_Watch_List]): A list of Stock_On_Watch_List objects representing
      the stocks to retrieve the current price for.

    Returns:
    - str: The current price of each stock as a string.

    This function iterates over the provided list of stocks and retrieves the current price
    for each stock. It uses PyAutoGUI to capture a screenshot of the stock's price region
    on the screen. The screenshot is then passed to PyTesseract for OCR (Optical Character
    Recognition) to extract the text from the image.

    The extracted stock price is then stripped of any leading or trailing whitespace using
    the `strip` method. If a stock price is successfully extracted, it is immediately returned
    as a string. If no stock price is found (empty string), the function returns False.

    Note: The assumption is made that each stock's price is displayed as text within a defined
    region on the screen, and OCR is used to extract that text. Adjustments to the region or
    OCR settings may be necessary based on the specific layout and characteristics of the
    stock price display.
    """
    for stock in stocks:
        # Take a screenshot of stock's price
        screenshot_stock_price = pyautogui.screenshot(region=(stock.upper_left_x, stock.upper_left_y, stock.lower_right_x - stock.upper_left_x, stock.lower_right_y - stock.upper_left_y))

        # Perform OCR on the screenshot image
        stock_price = pytesseract.image_to_string(screenshot_stock_price)

        stock_price.strip()

        if stock_price:
            return stock_price
        else:
            return False