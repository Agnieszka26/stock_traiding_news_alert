## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
import os
import html
import requests
import dotenv
from datetime import datetime, timedelta
dotenv.load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
ALPHAVANTAGE_FUNCTION = "TIME_SERIES_DAILY"
SERIES_NAME = "Time Series (Daily)"

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_last_two_trading_days():
    '''Ensure that the most recent trading days are fetched and return that date string formatted in list.'''
    now = datetime.now()
    days_checked = 0
    trading_days = []
    while len(trading_days) <2:
        date_stamp_formated = (now - timedelta(days=days_checked)).strftime('%Y-%m-%d')
        if date_stamp_formated in data[SERIES_NAME]:
            trading_days.append(date_stamp_formated)
        days_checked+=1
    return trading_days

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

def get_news():
    '''Get the first 3 news pieces for the COMPANY_NAME return in formatted way. '''
    news_params = {
        'apiKey':NEWS_API_KEY,
        'q': COMPANY_NAME,
    }
    news_url =  "https://newsapi.org/v2/everything"
    response = requests.get(url=news_url, params=news_params)
    news_data = response.json()
    news = news_data['articles']
    news = news[slice(0, 3)]
    news_formatted = []
    for info in news:
        news_formatted.append({
            "headline": html.unescape(info["title"]),
            "description": html.unescape(info["description"])
        })

    return news_formatted


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
def send_message(news, delta):
    for n_ in news:
        message = f'{STOCK}: {delta}% \nHeadline: {n_['headline']}\nBrief:{n_['description']}'
        print(message)

alphavantage_url = "https://www.alphavantage.co/query"
alphavantage_params = {
    'function':ALPHAVANTAGE_FUNCTION,
    'symbol': STOCK,
    'apikey':ALPHAVANTAGE_API_KEY
}
r = requests.get(url=alphavantage_url, params=alphavantage_params)
data = r.json()
if SERIES_NAME not in data:
    print(f"Error: Could not fetch stock data. {data['Information']}")
else:
    try:
        yesterday_formated, day_before_yesterday_formatted = get_last_two_trading_days()
        yesterday_open = float(data[SERIES_NAME][yesterday_formated]["1. open"])
        day_before_yesterday_open = float(data[SERIES_NAME][day_before_yesterday_formatted]["1. open"])
        delta_percent = round((yesterday_open - day_before_yesterday_open) * 100 / day_before_yesterday_open, 3)

        n = get_news()
        send_message(n, delta_percent)
        print(delta_percent)
        if abs(delta_percent) > 5:
            n = get_news()

            print("get news")


    except KeyError:
        print("Error: Missing stock data for required dates.")










#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

