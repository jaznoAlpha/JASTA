class ClickLocation:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MilTime:
    def __init__(self, hour, minute, second, microsecond):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond

class FocusedShare:
    def __init__(self, name, upper_left_coordinates, lower_right_coordinates):
        self.name = name
        self.upper_left_coordinates = upper_left_coordinates
        self.lower_right_coordinates = lower_right_coordinates

class Stock_On_Watch_List:
    def __init__(self, name, ticker, yahooURL, upper_left_x, upper_left_y, lower_right_x, lower_right_y):
        self.name = name
        self.ticker = ticker
        self.yahooURL = yahooURL
        self.upper_left_x = upper_left_x
        self.upper_left_y = upper_left_y
        self.lower_right_x = lower_right_x
        self.lower_right_y = lower_right_y