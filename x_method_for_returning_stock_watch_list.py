from z_classes import Stock_On_Watch_List
from typing import List

# Create instances of stock located on watch list - each tab is like 42px tall
MSFT  = Stock_On_Watch_List("Microsoft", "MSFT", "MSFT", 560, 170, 645, 215)
COST  = Stock_On_Watch_List("Costco", "COST", "COST", 560, 215, 645, 260)
VZ  = Stock_On_Watch_List("Verizon", "VZ", "VZ", 560, 260, 645, 305)
T  = Stock_On_Watch_List("AT&T", "T", "T", 560, 305, 645, 350)
XOM  = Stock_On_Watch_List("EXXON Mobil", "XOM", "XOM", 560, 350, 645, 395)
CVS  = Stock_On_Watch_List("CVS Pharmacies", "CVS", "CVS", 560, 395, 645, 440)
PEP  = Stock_On_Watch_List("Pepsi", "PEP", "PEP", 560, 440, 645, 485)
C  = Stock_On_Watch_List("Citigroup Inc.", "C", "Citi", 560, 485, 645, 530)
JPM  = Stock_On_Watch_List("JP Morgan & Chase", "JPM", "JPM", 560, 530, 645, 575)
BAC  = Stock_On_Watch_List("Bank of America", "BAC", "BAC", 560, 575, 645, 620)
WBD  = Stock_On_Watch_List("Warner Bros & Discover", "WBD", "WBD", 560, 620, 645, 665)
CMCSA  = Stock_On_Watch_List("Comcast", "CMCSA", "CMCSA", 560, 665, 645, 710)
DIS  = Stock_On_Watch_List("Disney", "DIS", "DIS", 560, 710, 645, 750)
MCD  = Stock_On_Watch_List("Mcdonalds", "MCD", "MCD", 560, 750, 645, 795)
DOW  = Stock_On_Watch_List("DOW Chemicles", "DOW", "DOW", 560, 795, 645, 840)
WMT  = Stock_On_Watch_List("Walmart", "WMT", "WMT", 560, 840, 645, 885)
TGT  = Stock_On_Watch_List("Target", "TGT", "TGT", 560, 885, 645, 930)
TSLA  = Stock_On_Watch_List("Tesla", "TSLA", "TSLA", 560, 930, 645, 975)
GOOG  = Stock_On_Watch_List("Alphabet/Google", "GOOG", "GOOG", 560, 975, 645, 1020)
AMD  = Stock_On_Watch_List("Advanced Micro Devices (AMD)", "AMD", "AMD", 560, 1020, 645, 1060)
INTC  = Stock_On_Watch_List("Intel", "INTC", "INTC", 560, 1060, 645, 1105)
NVDA  = Stock_On_Watch_List("Nvidia", "NVDA", "NVDA", 560, 1105, 645, 1150)
AMZN  = Stock_On_Watch_List("Amazon", "AMZN", "AMZN", 560, 1150, 645, 1190)
KO  = Stock_On_Watch_List("Coca-Cola", "KO", "KO", 560, 1190, 645, 1235)
BBY  = Stock_On_Watch_List("Best Buy", "BBY", "BBY", 560, 1235, 645, 1280)
AAPL  = Stock_On_Watch_List("Apple", "AAPL", "AAPL", 560, 1280, 645, 1320)

# Create an array of objects
stock_watch_list = [MSFT, COST, VZ, T, XOM, CVS, PEP, C, JPM, BAC, WBD, CMCSA, DIS, MCD, DOW, WMT, TGT, TSLA, GOOG, AMD, INTC, NVDA, AMZN, KO, BBY, AAPL]

def return_stock_watch_list(*tickers) -> List[Stock_On_Watch_List]:

    """
    Returns a list of Stock_On_Watch_List objects based on the provided tickers.

    Args:
        *tickers: Variable-length argument list of tickers (strings).

    Returns:
        List[Stock_On_Watch_List]: List of Stock_On_Watch_List objects matching the tickers.
        If no tickers are provided, it returns all Stock_On_Watch_List objects.

    Example:
        return_stock_watch_list()  # Returns all Stock_On_Watch_List objects
        return_stock_watch_list("MSFT", "BBY")  # Returns objects with the tickers "MSFT" and "BBY"

    Stock_On_Watch_List Object:
        Represents a stock on a watch list.

        Properties:
        - name (str): The name of the stock.
        - ticker (str): The stock ticker symbol.
        - upper_left_x (int): The x-coordinate of the upper-left position on the watch list.
        - upper_left_y (int): The y-coordinate of the upper-left position on the watch list.
        - lower_right_x (int): The x-coordinate of the lower-right position on the watch list.
        - lower_right_y (int): The y-coordinate of the lower-right position on the watch list.
    """

    if not tickers:  # If no tickers are provided, return all objects
        return stock_watch_list
    else:
        return [obj for obj in stock_watch_list if obj.ticker in tickers]