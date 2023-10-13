from z_classes import ClickLocation

import pyautogui
import pytesseract
import time
import os

from typing import Optional, Tuple
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the target coordinates for clicking
vs_code_toolbar = ClickLocation(700, 20)
chrome_taskbar_shortcut = ClickLocation(1285, 1405)
chrome_new_window = ClickLocation(1205, 1115)
ibka_login_button = ClickLocation(625, 800)
ibka_welcome_screen_upper_left = ClickLocation(12, 970)
ibka_welcome_screen_lower_right = ClickLocation(270, 1004)


# If an action needs a delay, it will use this delay.
delay = 0.1
simulated_loading_delay = 4

def startup_setup_windows() -> bool:
    """
    Performs the startup setup for the Windows operating system.
    Assumes that the script is executed with VS Code taking up the left half of the screen.
    The function performs a series of actions such as window layout adjustments, opening browsers,
    logging into specific websites, and locating and interacting with elements on the screen.

    This function follows the following steps:
    1. Repositions VS to the right section of the screen layout.
    2. Opens up IBKA for live watchlist, does all setup work to navigate to list. Waits for user to complete 2FA security check.
    3. Opens up Robinhood to make trades which requires it take up center portion of screen.
    4. If it does those steps, it should return True which means it has successfully setup all screens!

    RETURN: This function will either return true which means it has completed setting up all of its windows
            and that JASTA is now ready to to performa any other action.
    """
    # This adds a slight delay after the script has started
    time.sleep(delay)

    # Move the mouse to the title bar of VS code -- Assumes VS Code is taking up left half of screen.
    pyautogui.moveTo(vs_code_toolbar.x, vs_code_toolbar.y)
    time.sleep(delay)

    # left clicks make sure VS code window is selected
    pyautogui.click()
    time.sleep(delay)

    # This is the windows shortcut that brings up window layout screen
    pyautogui.hotkey('win', 'z')
    time.sleep(delay)

    # Press 6 to choose layout
    pyautogui.press('3')
    time.sleep(delay)

    # Press 3 to have VS Code take up right section of the screen.
    pyautogui.press('2')
    time.sleep(delay)

    # Move the mouse to chrome taskbar shortcut
    pyautogui.moveTo(chrome_taskbar_shortcut.x, chrome_taskbar_shortcut.y)
    time.sleep(delay)

    # right clicks to bring up the context menu so it can select the "open new window" button
    pyautogui.rightClick()
    time.sleep(delay)

    # Move the mouse to open a new window
    pyautogui.moveTo(chrome_new_window.x, chrome_new_window.y)
    time.sleep(delay)

    # left clicks to open a new window
    pyautogui.click()
    time.sleep(delay)

    # Type IBKA url
    pyautogui.typewrite('https://ndcdyn.interactivebrokers.com/sso/Login')
    time.sleep(delay)

    # Press the Enter key
    pyautogui.press('enter')

    # there will also be an extended delay here to account for loading time of the webpage
    time.sleep(simulated_loading_delay)

    # This is the windows shortcut that brings up window layout screen
    pyautogui.hotkey('win', 'z')
    time.sleep(delay)

    # Press 6 to choose layout
    pyautogui.press('3')
    time.sleep(delay)

    # Press 3 to have IBKA window take up left section of the screen.
    pyautogui.press('1')
    time.sleep(delay)

    # Move the mouse to the login button of IBKA
    pyautogui.moveTo(ibka_login_button.x, ibka_login_button.y)
    time.sleep(delay)

    # left click on login button -- This assumed autofill is working correctly
    pyautogui.click()
    time.sleep(simulated_loading_delay)

    # The following while loop waits for user to finish logging in and complete the 2FA check
    expected_text = "Your Dashboard"

    while True:

        # Take a screenshot of area that should say "Welcome to IBKA"
        screenshot_welcome_ibka = pyautogui.screenshot(region=(ibka_welcome_screen_upper_left.x, ibka_welcome_screen_upper_left.y, ibka_welcome_screen_lower_right.x - ibka_welcome_screen_upper_left.x, ibka_welcome_screen_lower_right.y - ibka_welcome_screen_upper_left.y))

        # Perform OCR on the screenshot image
        welcome_ibka = pytesseract.image_to_string(screenshot_welcome_ibka)

        if welcome_ibka.strip() == expected_text:
            # Found expected text
            print("Success: Welcome message found.")
            break

        else:
            # Currently waiting for user to complete 2FA check
            print("Waiting on 2FA, please complete security check")

        print(welcome_ibka)
        time.sleep(delay)

    # Move the mouse to chrome taskbar shortcut
    pyautogui.moveTo(chrome_taskbar_shortcut.x, chrome_taskbar_shortcut.y)
    time.sleep(delay)

    # right clicks to bring up the context menu so it can select the "open new window" button
    pyautogui.rightClick()
    time.sleep(delay)

    # Move the mouse to open a new window of chrome
    pyautogui.moveTo(chrome_new_window.x, chrome_new_window.y)
    time.sleep(delay)

    # left clicks to open new window
    pyautogui.click()
    time.sleep(delay)

    # Navigate to Robinhood
    pyautogui.typewrite('robinhood.com')
    time.sleep(delay)

    # Press the Enter key
    pyautogui.press('enter')

    # there will also be an extended delay here to account for loading time of the webpage
    time.sleep(simulated_loading_delay)

    # This is the windows shortcut that brings up window layout screen
    pyautogui.hotkey('win', 'z')
    time.sleep(delay)

    # Press 6 to choose layout
    pyautogui.press('3')
    time.sleep(delay)

    # Press 3 to have Robinhood window take up center section of the screen.
    pyautogui.press('3')
    time.sleep(delay)

    # Move the mouse to clear spot on IBKA website
    pyautogui.moveTo(400, 230)
    time.sleep(delay)

    # left click to make sure IBKA window active
    pyautogui.click()
    time.sleep(delay)

    # Press the down key until watchlist_finder_image.png is found
    while True:
        print("scrolling down")
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        print("finished scrolling")


        watchlist_finder_image_path = "watchlist_finder_image.png"
        watchlist_finder_image_path_result = find_image(watchlist_finder_image_path)
        if watchlist_finder_image_path_result:
            watchlist_x, watchlist_y = watchlist_finder_image_path_result  # Extracting x and y coordinates
            print(f"Success: Found button for watchlist: {watchlist_finder_image_path_result}")
            break  # Exit the loop if the image is found
        else:
            print("Button for watchlist not found, continuing to scroll...")

    # Move the mouse to click on watchlist
    pyautogui.moveTo(385, watchlist_y)
    time.sleep(delay)

    # left click pull up watchlist
    pyautogui.click()
    time.sleep(delay)

    # Move the mouse to clear spot on IBKA website
    pyautogui.moveTo(800, 400)
    time.sleep(delay)

    # left click to make sure IBKA window active
    pyautogui.click()
    time.sleep(simulated_loading_delay)

    # Press the down key 45 times to find watchlist
    for _ in range(8):
        pyautogui.press('down')
        time.sleep(delay)

    # This is to account for the time it takes to scroll
    time.sleep(simulated_loading_delay)

    # Move mouse so clean screen can be captured
    pyautogui.moveTo(2115, 650)
    time.sleep(delay)

    watchlist_completed_image_path = "watchlist_completed.png"
    watchlist_completed_image_path_result = find_image(watchlist_completed_image_path)
    if watchlist_completed_image_path_result:
        print(f"Success: Completed startup process!: {watchlist_completed_image_path_result}")
        return True
    else:
        print("Error: Completed watchlist on IBKA not found")
        return False

def find_image(image_path: str) -> Optional[Tuple[int, int]]:
    """
    Locates the specified image on the screen and returns the coordinates of its center.
    
    Parameters:
    - image_path (str): The path to the image file to be located on the screen.
    
    Returns:
    - Tuple[int, int] or None: The coordinates (x, y) of the center of the located image,
      or None if the image is not found.
    
    This function uses PyAutoGUI's `locateOnScreen` function to search for the specified image
    on the screen. If the image is found, the function retrieves the coordinates of its center
    using the `center` method. The function then returns a tuple of the x and y coordinates.
    
    If the image is not found, the function returns None.
    """
    # Get the full path of the image file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_file = os.path.join(script_dir, "images_for_pytesseract", image_path)

    try:
        location = pyautogui.locateOnScreen(image_file)
        if location is not None:
            center = pyautogui.center(location)
            return center
    except pyautogui.ImageNotFoundException:
        return None