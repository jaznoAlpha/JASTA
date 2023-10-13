from x_methods_for_starting_up import startup_setup_windows
from x_method_for_handling_ibka import return_current_price_of_stock
from x_method_for_handling_stock_purchase_decision import decide_what_to_do_about_current_price
from x_method_for_handling_what_happens_after_analysis import method_for_handling_what_happens_after_analysis
from x_method_for_returning_stock_watch_list import return_stock_watch_list

from z_classes import MilTime

import time
import datetime

ticker = "CMCSA"  # Replace with the desired ticker symbol

use_custom_time_range = False
custom_start_time = MilTime(7, 30, 5, 0)
custom_end_time = MilTime(8, 50, 5, 0)

time_that_market_opens_at = MilTime(7, 30, 5, 0)
time_that_market_closes_at = MilTime(14, 0, 5, 0)

focused_stock_list = return_stock_watch_list(ticker)
focused_stock = focused_stock_list[0]
current_price_of_focused_stock = return_current_price_of_stock(focused_stock_list)

if use_custom_time_range:
    begin_at = custom_start_time
    end_at = custom_end_time
else:
    begin_at = time_that_market_opens_at
    end_at = time_that_market_closes_at


# Specify the start and end time for the loop in military format (24-hour clock)
start_time = datetime.datetime.now().replace(hour=begin_at.hour, minute=begin_at.minute, second=begin_at.second, microsecond=begin_at.microsecond)
end_time = datetime.datetime.now().replace(hour=end_at.hour, minute=end_at.minute, second=end_at.second, microsecond=end_at.microsecond)
current_time = datetime.datetime.now()

def startup():
    # Gives a second delay before startup to account for any lingering mouse movements by user
    time.sleep(1)

     # Get the current time
    current_time = datetime.datetime.now()

    # Checks to see if the end time is correct and set to after the current time
    # This was primarily to make sure the loop doesn't continue forever and has an end point.
    if(end_time > current_time):

    # Sets up all windows needed for JASTA
        if startup_setup_windows():
        
            # Print success message this stage is complete
            print("Success: All windows pulled up successfully and program is ready to begin.")
    
            # Get the current time
            current_time = datetime.datetime.now()
    
            # Check if the current time is already past the start time
            if current_time > start_time:
            
                # Calculate the time difference until the next minute with the same seconds and milliseconds as start_time
                time_difference = datetime.timedelta(minutes=1) - datetime.timedelta(seconds=start_time.second, milliseconds=start_time.microsecond)
                
                # Sleep until the next minute with the same seconds and milliseconds as start_time
                time.sleep(time_difference.total_seconds())
            
            # Update current time after the sleep
            current_time = datetime.datetime.now()
            
            # Breaks the loop once it's supposed to end and begins the minute by minute analysis
            if current_time >= start_time:
                print(f"Analysis began at {current_time}")
                minute_by_minute_analysis()
    
        # If the startup_setup_windows() failed to set up the correct windows in the correct spot then it will return False and shouold end the analysis with a printed error.
        else:
            print("Failed setting up windows!")

    # If the end time has already occured for that day then it will stop the analysis and print this error
    else:
        print("Error: Please pick an end time that is later than the current time")

def minute_by_minute_analysis():
    # Define the initial start time
    start_time = datetime.datetime.now()

    # Repeat the action within the specified time range
    while True:
        # update current time
        current_time = datetime.datetime.now()
        # Format the current time in standard American time
        formatted_time = current_time.strftime("%I:%M:%S %p")
        # Update current price of the focused stock
        current_price_of_focused_stock = return_current_price_of_stock(focused_stock_list)
        # Update start time for the next iteration
        start_time = current_time.replace(second=5, microsecond=0)

        # Print the extracted text
        print(f"At {formatted_time} {focused_stock.name} was ${current_price_of_focused_stock} per share")
        decision = decide_what_to_do_about_current_price(focused_stock_list, "option1")
        if(decision == "buy"):
            print(f"Analysis has determined that we should immediately buy {focused_stock.name} stock")
        elif(decision == "hold"):
            print(f"Analysis has determined that we should currently hold and not buy/sell")
        elif(decision == "sell"):
            print(f"Analysis has determined that we should immediately sell {focused_stock.name} stock")
        else:
            print(f"Error: Something unexpected happened at the decide_what_to_do_about_current_price function")

        # update current time
        current_time = datetime.datetime.now()

        # Calculate the elapsed time since the last iteration
        elapsed_time = current_time - start_time

        # Breaks the loop once its supposed to end.
        if current_time >= end_time:
            print(f"Analysis ended at {current_time}")
            break

        # Sleep until one minute has elapsed
        time_to_sleep = datetime.timedelta(minutes=1) - elapsed_time
        if time_to_sleep.total_seconds() > 0:
            time.sleep(time_to_sleep.total_seconds())
    
    #Trading day has ended, this method is called to wrap things up
    method_for_handling_what_happens_after_analysis()

startup()
