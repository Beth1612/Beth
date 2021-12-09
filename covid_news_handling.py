'''This module collects news articles using a covid api'''

import time
import json
import requests

config_data = json.load(open("config.json"))

def news_API_request(covid_terms = "Covid COVID-19 coronavirus"):
    '''Uses a news api to recieve news articles and returns this data'''
    base_url = "https://newsapi.org/v2/everything?"
    api_key = config_data["data"]["api_key"]
    complete_url = base_url +"q=" + covid_terms + "&apiKey=" + api_key
    response = requests.get(complete_url)
    response= response.json()
    return response

def update_news(cancel_news = []):
    '''A function that creates and returns a list of dictionaries that include the news articles by calling news_API_request and taking cancel_news so no unwanted articles are included'''
    news = []
    response = news_API_request(config_data["data"]["news_terms"])
    for n in range (len(response["articles"])):
        if response["articles"][n]["title"] not in cancel_news and len(news) < 4:
            news.append({"title":(response["articles"][n]["title"]),"content":((response["articles"][n]["description"])+" "+(response["articles"][n]["url"]))})
    return news

def schedule_news_updates(update_interval,update_name,s):
    '''Creates schedule updates of the news articles and returns the name of the update created'''
    globals()[update_name] = s.enterabs(time.time()+update_interval,1,update_news,)
    return globals()[update_name]
