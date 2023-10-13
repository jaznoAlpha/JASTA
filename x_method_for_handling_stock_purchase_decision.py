import time

def decide_what_to_do_about_current_price(focused_stock_list, current_price: str) ->str:
    if current_price == 'option1':
        time.sleep(15)
        return 'buy'
    elif current_price == 'option2':
        return 'hold'
    elif current_price == 'option3':
        return 'sell'
    else:
        return False