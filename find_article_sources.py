#from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
import os
from datetime import datetime, timedelta

#from dotenv import load_dotenv
# Load environment variables from .env file
#load_dotenv()

today = datetime.today().date()
date = today - timedelta(days=1)

#news_api_key = os.getenv("NEWSAPI_API_KEY")
def findarticlesources():
    news_api_key = os.getenv("NEWSAPI_API_KEY")
    newsapi = NewsApiClient(api_key = news_api_key)
    all_articles = newsapi.get_everything(q='Tennis',
                                        from_param=date,
                                        #sources= 'NDTV News, cbc-news, espn',
                                        #domains=,
                                        language='en',
                                        sort_by='relevancy',
                                        page=1)
    print(json.dumps(all_articles, indent=4))

        # Initialize an empty list to store the URLs
    # Loop through each item in the JSON data and extract the 'url' field
    articles_info = [
    {
        'title': article['title'],
        'url': article['url'],
        'publishedAt': article['publishedAt'],
        'author': article['author'],
        'source': article['source']['name']
    }
    for article in all_articles['articles']
    ]
    
    
    #urls = [article['url'] for article in all_articles['articles']]
    #titles = [article['title'] for article in all_articles['articles']]
    #print(urls)
    print(articles_info)
    pretty_data = json.dumps(articles_info, indent=4)
    print(pretty_data)
    return(articles_info)
findarticlesources()