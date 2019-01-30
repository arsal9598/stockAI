"""
Use IEXTrading to gather real-time stock data for AI
"""
import requests
import struct
import json
import csv
import pandas as pd
from datetime import datetime as dt

endpoint = "https://api.iextrading.com/1.0"

###############
# main function
###############
def create_csv(company):
    """
    Parameter is company symbol Takes Dict from get_marketOpen_historical_data(company)
    and makes csv file to use as data to feed neural network
    """
    # write dictonary to csv file
    mydict = get_marketOpen_historical_data(company)
    mydict2 = get_high_and_low(company)
    mydict3 = get_close_and_volume(company)
    mydict4 = get_change_and_changepercent(company)
    mydict5 = get_vwap_and_changeovertime(company)
    with open(company + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for (k,v), (k2,v2), (k3,v3), (k4, v4), (k5, v5) in zip(mydict.items(), mydict2.items(), mydict3.items(), mydict4.items(), mydict5.items()):
            writer.writerow([k, v, k2, v2, k3, v3, k4, v4, k5, v5])

    # use pandas to add headernames cause DictWriter is gay
    df = pd.read_csv(company + '.csv', header=None)
    df.rename(columns={0: 'date', 1: 'open', 2: 'low', 3: 'high', 4: 'close', 5: 'volume', 6: 'change', 7: 'changePercent', 8: 'vwap', 9: 'changeOverTime'}, inplace=True)
    df.to_csv(company + '.csv', index=False)


#######################
# main helper Functions
#######################

def get_marketOpen_historical_data(company):
    """
    Parameter is company symbol. Loops through time since companies IPO
    and records "open" and "date" keys, writes it into dict and returns.
    """

    # get json data from IEX API
    response = requests.get(endpoint + "/stock/" + company + "/chart/5y")
    data = response.json()

    # grab date and price values and add to dict
    dict = {}
    for vals in data:
        date = ""
        open = ""
        for key, value in vals.items():
            if key == "date":
                date = get_toordinal(value)
            if key == "open":
                open = value
            dict[date] = open
    return dict

def get_high_and_low(company):
    """
    Parameter is company symbol. Loops through time since IPO
    and grabs the high and low and returns a dict with both vals
    """
    # get json data from IEX API
    response = requests.get(endpoint + "/stock/" + company + "/chart/5y")
    data = response.json()
    # grabs low and high values and add to dict
    dict = {}
    for vals in data:
        low = ""
        high = ""
        for key, value in vals.items():
            if key == "low":
                low = value
            if key == "high":
                high = value
        dict[low] = high
    return dict

def get_close_and_volume(company):
    """
    Parameter is company. Loops through time since IPO and grabs
    close and volume stats and returns dict with both of em
    """
    # get json data from IEX API
    response = requests.get(endpoint + "/stock/" + company + "/chart/5y")
    data = response.json()
    # grabs low and high values and add to dict
    dict = {}
    for vals in data:
        close = ""
        volume = ""
        for key, value in vals.items():
            if key == "close":
                close = value
            if key == "volume":
                volume = value
        dict[close] = volume
    return dict

def get_change_and_changepercent(company):
    """
    Parameter is company. Loops through time since IPO and grabs
    change and change percent stats and returns dict with both of em
    """
    # get json data from IEX API
    response = requests.get(endpoint + "/stock/" + company + "/chart/5y")
    data = response.json()
    # grabs low and high values and add to dict
    dict = {}
    for vals in data:
        change = ""
        change_percent = ""
        for key, value in vals.items():
            if key == "change":
                change = value
            if key == "changePercent":
                change_percent = value
        dict[change] = change_percent
    return dict

def get_vwap_and_changeovertime(company):
    """
    Parameter is company. Loops through time since IPO and grabs
    vwap and change over time stats and returns dict with both of em
    """
    # get json data from IEX API
    response = requests.get(endpoint + "/stock/" + company + "/chart/5y")
    data = response.json()
    # grabs low and high values and add to dict
    dict = {}
    for vals in data:
        vwap = ""
        change_over_time = ""
        for key, value in vals.items():
            if key == "vwap":
                vwap = value
            if key == "changeOverTime":
                change_over_time = value
        dict[vwap] = change_over_time
    return dict

#######################
# misc. helper functions
#######################

def get_price(company):
    """
    Parameter is company symbol, returns current stock price
    """
    # get api data from IEX and convert to float
    response = requests.get(endpoint + "/stock/" + company + "/price")
    price = float(response.content.decode("utf8"))

    return price

def get_toordinal(date):
    """
    Parameter is date return number of days since year 1 day 1
    """
    d = dt.strptime(date, '%Y-%m-%d').date()
    return d.toordinal()

def get_news(company, name):
    """
    Parameter is company symbol and actual name, returns some company news headlines as list
    """
    # get api data from IEX and convert to float
    response = requests.get(endpoint + "/stock/" + company + "/news/last/50")
    data = response.json()

    news = {}
    for vals in data:
        headline = ""
        datetime = ""
        for key, value in vals.items():
            if key == "headline":
                if name.lower() in value.lower():
                    headline = value
                else:
                    headline = "None"
            if key == "datetime":
                datetime = value
        news[datetime] = headline
    return news

create_csv("aapl")
