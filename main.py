import sys
import requests
import time 
import schedule
import datetime
# Main packages
import json
import yfinance as f
import urllib.parse
# Telegram config file
#import telegram_config as cfg

class Telegram_stock:
    def __init__(self,symbol,timer,token,chat):
        self.symbol = symbol
        self.timer = timer
        self.token = token
        self.chat = chat

    def check_len_symbol(self):
        if len(self.symbol) <= 1:
            print('Input a valid stock symbol. Ex: "TSLA" ')
            quit()
        else:
            pass

    def run_script_timer(self):
        if len(self.timer) <= 2:
            # 60 seconds
            repeat = 60
        elif int(self.timer) >= 1:
            repeat = int(self.timer)
        else:
            print('Input a valid re-run script integer.')
            quit()

    def getstock(self):
        # Check if telegram tokens are valid
        if len(self.token) > 40 and len(self.chat) > 5:
            pass
        else:
            print('Telegram config invalid.')
            quit()



        # Fetch stock symbol currency
        for l in self.symbol:
            currency = ''
            price = 0
            prev_price = 0

            stock_meta_data = f.Ticker(l)
            stock_dict = stock_meta_data.info
            stock_json = json.dumps(stock_dict)
            stock_json = json.loads(stock_json)
            if stock_json["currency"] != '':
                currency = stock_json["currency"]


            # Time to get the stock
            stock = f.download(l, period = '1d')

            if prev_price == 0:
                prev_price = stock["Open"][0].round(3)
            else:
                prev_price = price
            price = stock["Close"][0].round(3)

            if prev_price == 0 or price == prev_price:
                price_change_str = " "
                price_diff_str = " "
            elif price > prev_price:
                price_diff = (price - prev_price).round(3)
                price_change_str = "Price Rise"
                price_diff_str = "("+price_change_str+" +"+str("{0:,.2f}".format(price_diff)).replace(',', '\'')+")"
            elif price < prev_price:
                price_diff = (prev_price- price).round(3)
                price_change_str = "Price DROP"
                price_diff_str = "("+price_change_str+" -"+str("{0:,.2f}".format(price_diff)).replace(',', '\'')+")"

            # Build message string with escaping url critical chars
            message=l+"@ *"+currency+" "+str("{0:,.2f}".format(price)).replace(',', '\'')+"* "+price_diff_str
            message=message.replace("-","\-")
            message=message.replace("+","\+")
            message=message.replace(".","\.")
            message=message.replace("(","\(")
            message=message.replace(")","\)")
            message=message.replace("?","\?")
            message=message.replace("^","\^")
            message=message.replace("$","\$")
            message=urllib.parse.quote_plus(message)

            # Send GET request to Telegram Bot API
            send='https://api.telegram.org/bot' + self.token + '/sendMessage?parse_mode=MarkdownV2&disable_notification=true&chat_id=' + self.chat + '&text=' + message
            #DEBUG: print(send)
            response=requests.get(send)
            time.sleep(0.1)

    def main(self):
        import threading

        while True:
            self.getstock()
            time.sleep(self.timer)
if __name__ == '__main__':
    symbol = ['TSLA','AAPL','NVDA']
    timer = 30
    token = '1768949581:AAF4hIwvBq2vgBTurf8owlFAWJPtmhGrsQQ'
    chat = '1724783850'
    bot = Telegram_stock(symbol,timer,token,chat)
    bot.main()