from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
# Load environment variables from .env file
load_dotenv()

date = '2024-10-01'
#news_api_key = os.getenv("NEWSAPI_API_KEY")
def findarticlesources():
    news_api_key = "87e00ea51cf440758b04ee8a73ae892d"
    newsapi = NewsApiClient(api_key = news_api_key)
    all_articles = newsapi.get_everything(q='Tennis',
                                        from_param=date,
                                        sources='espn',
                                        #domains=,
                                        language='en',
                                        sort_by='relevancy',
                                        page=1)
    print(json.dumps(all_articles, indent=4))

        # Initialize an empty list to store the URLs
    # Loop through each item in the JSON data and extract the 'url' field
    urls = [article['url'] for article in all_articles['articles']]
    titles = [article['title'] for article in all_articles['articles']]
    #print(urls)
    print(titles)
    return(urls, titles)
findarticlesources()