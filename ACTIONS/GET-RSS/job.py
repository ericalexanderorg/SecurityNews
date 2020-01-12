#!/usr/bin/env python3
import requests
import xmltodict
from dateutil.parser import parse
import json
import os


def get_xml_feed(url):
    resp = requests.get(url)
    return xmltodict.parse(resp.text)

def add_rss_data(current_news, source, url, link_key="link"):
    feed = get_xml_feed(url)
    for item in feed['rss']['channel']['item']:
        new = {}
        new['Source'] = source
        new['Title'] = item['title']
        new['Date'] = '{}'.format(parse(item['pubDate']))
        #new['Description'] = item['description']
        new['URL'] = item[link_key]
        current_news.append(new)
    return current_news

def add_reddit_data(current_news, source, url):
    feed = get_xml_feed(url)
    #print(json.dumps(feed))
    # for entry in feed['rss']['channel']['item']:
    #     new = {}
    #     new['Source'] = source
    #     new['Title'] = item['title']
    #     new['Date'] = '{}'.format(parse(item['pubDate']))
    #     #new['Description'] = item['description']
    #     new['URL'] = item[link_key]
    #     current_news.append(new)
    # return current_news

# Create our lists
all_news = []
breach_news = []
tool_news = []
cve_news = []

# Run through our news feed sources and add to all news
all_news = add_rss_data(all_news, 'The Hacker News', "http://feeds.feedburner.com/TheHackersNews?format=rss", "feedburner:origLink")
all_news = add_rss_data(all_news, 'BleepingComputer', "https://www.bleepingcomputer.com/feed/")
all_news = add_rss_data(all_news, 'ITPro.', "https://www.itpro.co.uk/security/feed")
all_news = add_rss_data(all_news, 'Krebs On Security', "https://krebsonsecurity.com/feed/")
all_news = add_rss_data(all_news, 'Threatpost', "https://threatpost.com/feed/")
all_news = add_rss_data(all_news, 'Wired', "https://www.wired.com/feed/category/security/latest/rss")
#all_news = add_rss_data(all_news, 'Security Magazine', "https://www.securitymagazine.com/rss")
all_news = add_rss_data(all_news, 'SecurityWeek', "https://feeds.feedburner.com/securityweek", "feedburner:origLink")
all_news = add_rss_data(all_news, 'Naked Security', "https://feeds.feedburner.com/securityweek")
all_news = add_rss_data(all_news, 'KitPloit', "https://feeds.feedburner.com/PentestTools", "feedburner:origLink")
#all_news = add_reddit_data(all_news, 'reddit.com/r/InfoSecNews', "https://www.reddit.com/r/InfoSecNews.rss")
#all_news = add_reddit_data(all_news, 'reddit.com/r/netsec', "https://www.reddit.com/r/netsec.rss")
tool_news = add_rss_data(tool_news, 'Rapid7', 'https://blog.rapid7.com/rss/')
tool_news = add_rss_data(tool_news, 'KitPloit', "https://feeds.feedburner.com/PentestTools", "feedburner:origLink")
cve_news = add_rss_data(cve_news, 'Twitter: @CVEnew', 'https://rss.app/feeds/Noif7vQPp82HoFpd.xml')

# Pattern match on potential breach news and add to the breach_news list
patterns = ['ransomware', 'breach', 'exposed', 'cyber attack', 'hacked', 'hackers', 'skimming', 'magecart']
for item in all_news:
    for pattern in patterns:
        if pattern in item['Title'].lower():
            breach_news.append(item)


out = {
    'All News': all_news, 
    'Breach News': breach_news, 
    'Tool News': tool_news,
    'CVE News': cve_news
}
f = open("../../UI/v1/src/data.json", "w")
f.write(json.dumps(out))
f.close()

