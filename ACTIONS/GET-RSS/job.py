#!/usr/bin/env python3
import requests
import xmltodict
from dateutil.parser import parse
import json
import os
import gzip

def add_cve_data(current_news):
    # Download gunzipped json file of recent CVEs
    r = requests.get('https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.gz')
    with open('nvdcve-1.1-recent.json.gz', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    # gunzip and read json into data variable
    with gzip.open('nvdcve-1.1-recent.json.gz', 'rb') as f:
        data = json.loads(f.read())

    # Delete the temp file
    os.remove('nvdcve-1.1-recent.json.gz')

    # add to dict
    for cve in data['CVE_Items']:
        new = {}
        new['Source'] = 'nist.gov'
        new['Title'] = cve['cve']['description']['description_data'][0]['value']
        new['Date'] = '{}'.format(parse(cve['publishedDate']))
        new['URL'] = 'https://cve.mitre.org/cgi-bin/cvename.cgi?name={}'.format(cve['cve']['CVE_data_meta']['ID'])
        current_news.append(new)
    
    return current_news



def get_xml_feed(url):
    session = requests.Session()
    # Avoid getting blocked by Reddit due to the default requests agent string. 
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3945.117 Safari/537.36'})
    resp = session.get(url)
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
    for entry in feed['feed']['entry']:
        new = {}
        new['Source'] = source
        new['Title'] = entry['title']
        new['Date'] = '{}'.format(parse(entry['updated']))
        #new['Description'] = item['description']
        new['URL'] = entry['link']['@href']
        current_news.append(new)
    return current_news

# Create our lists
all_news = []
breach_news = []
tool_news = []
vuln_news = []

# Run through our news feed sources and add to all news
all_news = add_reddit_data(all_news, 'reddit.com/r/InfoSecNews', "https://www.reddit.com/r/InfoSecNews.rss")
all_news = add_rss_data(all_news, 'The Hacker News', "http://feeds.feedburner.com/TheHackersNews?format=rss", "feedburner:origLink")
all_news = add_rss_data(all_news, 'BleepingComputer', "https://www.bleepingcomputer.com/feed/")
all_news = add_rss_data(all_news, 'ITPro.', "https://www.itpro.co.uk/security/feed")
all_news = add_rss_data(all_news, 'Krebs On Security', "https://krebsonsecurity.com/feed/")
all_news = add_rss_data(all_news, 'Threatpost', "https://threatpost.com/feed/")
all_news = add_rss_data(all_news, 'Wired', "https://www.wired.com/feed/category/security/latest/rss")
#all_news = add_rss_data(all_news, 'Security Magazine', "https://www.securitymagazine.com/rss")
all_news = add_rss_data(all_news, 'SecurityWeek', "https://feeds.feedburner.com/securityweek", "feedburner:origLink")
all_news = add_rss_data(all_news, 'Security Affairs', "https://securityaffairs.co/wordpress/feed")
all_news = add_rss_data(all_news, 'Naked Security', "https://nakedsecurity.sophos.com/feed/")
all_news = add_rss_data(all_news, 'KitPloit', "https://feeds.feedburner.com/PentestTools", "feedburner:origLink")
all_news = add_rss_data(all_news, 'Securelist', "https://securelist.com/feed/")
#all_news = add_rss_data(all_news, 'OpenSecurity.global', "https://opensecurity.global/discover/all.xml/")
all_news = add_rss_data(all_news, 'Zero Day Initiative - Upcoming', "https://www.zerodayinitiative.com/rss/upcoming")
all_news = add_rss_data(all_news, 'Zero Day Initiative - Published', "https://www.zerodayinitiative.com/rss/published")
all_news = add_rss_data(all_news, 'Zero Day Initiative - Blog', "https://www.zerodayinitiative.com/blog?format=rss")
tool_news = add_rss_data(tool_news, 'Rapid7', 'https://blog.rapid7.com/rss/')
tool_news = add_rss_data(tool_news, 'KitPloit', "https://feeds.feedburner.com/PentestTools", "feedburner:origLink")
vuln_news = add_cve_data(vuln_news)
vuln_news = add_rss_data(vuln_news, 'Zero Day Initiative - Upcoming', "https://www.zerodayinitiative.com/rss/upcoming")
vuln_news = add_rss_data(vuln_news, 'Zero Day Initiative - Published', "https://www.zerodayinitiative.com/rss/published")
# Note on Reddit requests: They're staggered to avoid hitting their rate limit when we make 2 requests within 6 seconds
all_news = add_reddit_data(all_news, 'reddit.com/r/netsec', "https://www.reddit.com/r/netsec.rss")

# Pattern match on potential breach news and add to the breach_news list
patterns = ['ransomware', 'breach', 'exposed', 'attack', 'hacked', 'hackers', 'skimming', 'magecart']
for item in all_news:
    for pattern in patterns:
        if pattern in item['Title'].lower():
            breach_news.append(item)

# Pattern match on potential vulnerability news and add to the vuln_news list
patterns = ['0-day', 'zero-day', 'cve-']
for item in all_news:
    for pattern in patterns:
        if pattern in item['Title'].lower():
            vuln_news.append(item)


out = {
    'All News': all_news, 
    'Breach News': breach_news, 
    'Tool News': tool_news,
    'Vuln News': vuln_news
}
f = open("../../UI/v1/src/data.json", "w")
f.write(json.dumps(out))
f.close()

