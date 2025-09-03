import feedparser, hashlib
from datetime import datetime
from models.news import NewsItem



def fetch_bbc():
    BBC_RSS="https://feeds.bbci.co.uk/news/rss.xml"
    feed=feedparser.parse(BBC_RSS)
    items=[]

    for e in feed.entries:
        news_id=hashlib.md5(e.link.encode("utf-8")).hexdigest()

        if hasattr(e,"published_parsed") and e.published_parsed:
            ts=datetime(*e.published_parsed[:6])

        else:
            ts=datetime.utcnow()

        items.append(NewsItem(
            id=news_id,
            title=getattr(e,"title",""),
            description=getattr(e,"description",""),
            url=getattr(e,"link",""),
            source="BBC",
            published_at=ts,
            ))
    print("I am in connector.py")
    for i in items:
        print(i.title)
        
    return items


        
        
