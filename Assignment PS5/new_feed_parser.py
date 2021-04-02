import feedparser
d = feedparser.parse('http://news.google.com/news?output=rss')
print(d.feed.title)