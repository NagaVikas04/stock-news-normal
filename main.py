import requests
from datetime import datetime, timedelta
from twilio.rest import Client
from os import environ

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = environ['stock_api_key']

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = environ['news_api_key']

TWILIO_SID = environ['twilio_sid']
TWILIO_AUTH_TOKEN = environ['twilio_auth_token']

STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "5min",
    "apikey": STOCK_API_KEY
}

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

yesterday_datetime = datetime.now() - timedelta(5)
yesterday_date = yesterday_datetime.date()

day_before_yesterday_datetime = datetime.now() - timedelta(6)
day_before_yesterday_date = day_before_yesterday_datetime.date()

NEWS_API_PARAMS = {
    "q": COMPANY_NAME,
    # "from": day_before_yesterday_date,
    "apikey": NEWS_API_KEY
    # "language": "en",
    # "sortBy": "popularity"
}

response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMS)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
print(stock_data)

stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_stock_price = stock_data_list[2]["4. close"]
day_before_yesterdays_stock_price = stock_data_list[5]["4. close"]

# except KeyError:
#     print("No trading data available on one of the day or either of the days")
# else:

yesterday_stock_price = float(yesterday_stock_price)
day_before_yesterdays_stock_price = float(day_before_yesterdays_stock_price)
print(yesterday_stock_price, day_before_yesterdays_stock_price)

change_in_stock_price = yesterday_stock_price - day_before_yesterdays_stock_price
change_in_stock_price = abs(change_in_stock_price)
print(change_in_stock_price)

up_down = None
if change_in_stock_price > 0:
    up_down = "⬆"
else:
    up_down = "⬇"

change_in_percent = round((change_in_stock_price / yesterday_stock_price) * 100)
print(change_in_percent)

if change_in_percent > 5:
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_API_PARAMS)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    print(articles)

    first_three_articles = articles[:3]
    print(first_three_articles)

    formatted_articles = [
           f"{STOCK_NAME}: {up_down}{change_in_percent}% \nHeadline: {article['title']}. \nBreif: {article['description']}" for article in first_three_articles]
    print(formatted_articles)

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        print(article)
        message = client.messages.create(
            body=article,
            from_=environ['twilio_number'],
            to=environ['your_number']
        )
# TODO 2. - Get the day before yesterday's closing stock price

# day_before_yesterdays_stock_price = stock_data["Time Series (Daily)"][f"{day_before_yesterday_date}"]["4. close"]
# day_before_yesterdays_stock_price = float(day_before_yesterdays_stock_price)
# print(day_before_yesterdays_stock_price)

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
# change_in_stock_price = yesterday_stock_price - day_before_yesterdays_stock_price
# change_in_stock_price = abs(change_in_stock_price)
# print(change_in_stock_price)

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
# percentage = (change_in_stock_price/yesterday_stock_price)*100
# print(percentage)

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
# if percentage > 5:
#     print("Get News")

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

# TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
