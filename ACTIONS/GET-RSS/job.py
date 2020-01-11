#!/usr/bin/env python3
import requests
import xmltodict
from dateutil.parser import parse
#from datetime import datetime
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

# Create our lists
all_news = []
breach_news = []

# Run through our news feed sources and add to all news
all_news = add_rss_data(all_news, 'The Hacker News', "http://feeds.feedburner.com/TheHackersNews?format=rss", "feedburner:origLink")
all_news = add_rss_data(all_news, 'BleepingComputer', "https://www.bleepingcomputer.com/feed/")
all_news = add_rss_data(all_news, 'ITPro.', "https://www.itpro.co.uk/security/feed")
all_news = add_rss_data(all_news, 'Krebs On Security', "https://krebsonsecurity.com/feed/")
all_news = add_rss_data(all_news, 'Threatpost', "https://threatpost.com/feed/")

# Pattern match on potential breach news and add to the breach_news list
patterns = ['ransomware', 'breach', 'exposed', 'cyber attack', 'hacked', 'hackers', 'skimming', 'magecart']
for item in all_news:
    for pattern in patterns:
        if pattern in item['Title'].lower():
            breach_news.append(item)


out = {'All News': all_news, 'Breach News': breach_news}
f = open("../../UI/v1/src/data.json", "w")
f.write(json.dumps(out))
f.close()

