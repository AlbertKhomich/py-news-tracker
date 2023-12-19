import requests
import datetime as dt
from twilio.rest import Client


# Check increase/decrease by limit
def increase_check(day_1: float, day_2: float) -> bool:
    limit_rate = day_1 / 100 * RATE
    if abs(day_1 - day_2) >= limit_rate:
        return True
    else:
        return False


# Make a rating
def calculate_percent(day_1: float, day_2: float) -> str:
    if day_1 > day_2:
        return f"🔻%{round(float(((day_1 - day_2) * 100) / day_1), 2)}"
    else:
        return f"🔺%{round(float(((day_2 - day_1) * 100) / day_1), 2)}"


RATE = 2
STOCK = "NVDA"
COMPANY_NAME = "Nvidia"
ALPHA_VANTAGE_API_KEY = "777777777"
NEWS_API_KEY = "777777777777777"
account_sid = "7777777777777"
auth_token = "77777777777777777"

# Stocks api
params_alpha_vantage_api = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_API_KEY
}

url_stock = 'https://www.alphavantage.co/query'

r = requests.get(url_stock, params=params_alpha_vantage_api)
data = r.json()

# Close Bill by 2 days ago
today = dt.date.today()
yesterday = (today - dt.timedelta(days=1)).strftime('20%y-%m-%d')
day_before_yesterday = (today - dt.timedelta(days=2)).strftime('20%y-%m-%d')

yesterday_close = float(data["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_close = float(data["Time Series (Daily)"][day_before_yesterday]["4. close"])

# News api
url_news = "https://newsapi.org/v2/everything"

params_news = {
    "q": COMPANY_NAME,
    "from_param": day_before_yesterday,
    "to": yesterday,
    "language": 'en',
    "sortBy": "publishedAt",
    "apikey": NEWS_API_KEY
}

if increase_check(day_before_yesterday_close, yesterday_close):

    response = requests.get(url_news, params=params_news)
    news = response.json()

    # Three new news
    hot_news = {news["articles"][x]["title"]: news["articles"][x]["description"] for x in range(3)}

    rating = calculate_percent(day_before_yesterday_close, yesterday_close)

    # Send 3 SMS with rating and news
    for k, v in hot_news.items():
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"{COMPANY_NAME}: {rating}\nHeadline: {k}\nBrief: {v}",
            from_="+777777777",
            to="+77777777777"
        )
        print(message.sid)

else:
    print("You can sleep")
