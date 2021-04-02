## this is code is not used for ps5 but is used to find out how the version of feedparser works
import feedparser
d = feedparser.parse('http://news.google.com/news?output=rss')
print(d.feed.title)