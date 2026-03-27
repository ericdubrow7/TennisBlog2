#from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
# Load environment variables from .env file
#load_dotenv()

# How far back to search (more days = more potential articles)
DAYS_BACK = 2
# Number of pages to fetch (100 articles per page; free tier may limit total results)
MAX_PAGES = 3

# News API returns article "content" truncated to ~200 characters. To get full text we fetch the URL.
REQUEST_TIMEOUT = 15
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_full_article_content(url):
    """Fetch the article URL and extract full main text. Returns empty string on failure."""
    try:
        resp = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove script/style and other non-article elements
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()
        # Prefer semantic article containers
        for selector in ['article', '[itemprop="articleBody"]', 'main', '.article-body', '.post-content', '.entry-content']:
            container = soup.select_one(selector)
            if container:
                paragraphs = container.find_all("p")
                if paragraphs:
                    text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                    if len(text) > 100:
                        return text
        # Fallback: all paragraphs in the body
        body = soup.find("body") or soup
        paragraphs = body.find_all("p")
        text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return text if text else ""
    except Exception:
        return ""


def findarticlesources(fetch_full_content=True):
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
            item = {
                'title': article['title'],
                'url': url,
                'publishedAt': article.get('publishedAt', ''),
                'description': article.get('description') or '',
                'content': article.get('content') or ''  # News API truncates this to ~200 chars
            }
            if fetch_full_content:
                full = fetch_full_article_content(url)
                item['full_content'] = full if full else item['content']  # fallback to API snippet
            all_articles.append(item)
        # If we got fewer than page_size, there are no more pages
        if len(articles) < 100:
            break

    print(json.dumps({'total': len(all_articles), 'articles': all_articles}, indent=2))
    return all_articles


if __name__ == '__main__':
    findarticlesources()