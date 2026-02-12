#from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
import os
from datetime import datetime, timedelta
#from dotenv import load_dotenv
# Load environment variables from .env file
#load_dotenv()

# How far back to search (more days = more potential articles)
DAYS_BACK = 2
# Number of pages to fetch (100 articles per page; free tier may limit total results)
MAX_PAGES = 3

def findarticlesources():
    news_api_key = os.getenv("NEWSAPI_API_KEY")
    newsapi = NewsApiClient(api_key=news_api_key)

    from_date = (datetime.today().date() - timedelta(days=DAYS_BACK)).isoformat()

    # Collect articles from multiple pages; no 'sources' filter = all sources
    all_articles = []
    seen_urls = set()

    for page in range(1, MAX_PAGES + 1):
        response = newsapi.get_everything(
            q='Tennis',
            from_param=from_date,
            language='en',
            #sources='bbc-sport, espn, the-guardian-uk, reuters',
            sort_by='relevancy',
            page_size=100,
            page=page
        )
        articles = response.get('articles') or []
        if not articles:
            break
        for article in articles:
            url = article.get('url')
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            # Skip entries with no title (often removed/placeholder)
            if not (article.get('title') and article.get('title').strip()):
                continue
            all_articles.append({
                'title': article['title'],
                'url': url,
                'publishedAt': article.get('publishedAt', '')
            })
        # If we got fewer than page_size, there are no more pages
        if len(articles) < 100:
            break

    print(json.dumps({'total': len(all_articles), 'articles': all_articles}, indent=2))
    return all_articles


if __name__ == '__main__':
    findarticlesources()