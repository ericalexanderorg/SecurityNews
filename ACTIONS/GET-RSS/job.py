#!/usr/bin/env python3
import requests
import xmltodict
import json
import os

def get_xml_feed(url):
    resp = requests.get(url)
    return xmltodict.parse(resp.text)


news = []

source = 'The Hacker News'
feed = get_xml_feed("http://feeds.feedburner.com/TheHackersNews?format=rss")
for item in feed['rss']['channel']['item']:
    new = {}
    new['Source'] = source
    new['Title'] = item['title']
    new['Date'] = item['pubDate']
    #new['Description'] = item['description']
    new['URL'] = item['feedburner:origLink']
    news.append(new)



out = {'News': news}
f = open("../../UI/v1/src/data.json", "w")
f.write(json.dumps(out))
f.close()

