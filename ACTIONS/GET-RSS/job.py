#!/usr/bin/env python3
import requests
import xmltodict
import xml.etree.ElementTree
from xml.dom import minidom
import datetime
from dateutil.parser import parse
import json
import os
import gzip

def sort_uniq(news_list):
    temp_list = []
    for news in news_list:
        if news['Title'] not in temp_list:
            temp_list.append(news['Title'])
        else:
            news_list.remove(news)
    
    return news_list

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
        # Filter out anything that doesn't match this year
        cve_id = cve['cve']['CVE_data_meta']['ID']
        cve_year = cve_id.split("-")[1]
        now = datetime.datetime.now()
        if str(now.year) in cve_year:
            # Filter out everything that was rejected
            if "** REJECT **" not in cve['cve']['description']['description_data'][0]['value']:
                new = {}
                new['Source'] = 'nist.gov'
                new['Title'] = cve['cve']['description']['description_data'][0]['value']
                new['Date'] = '{}'.format(parse(cve['publishedDate']))
                new['URL'] = 'https://cve.mitre.org/cgi-bin/cvename.cgi?name={}'.format(cve['cve']['CVE_data_meta']['ID'])
                new['Impacts'] = '?'
                new['HasCVSS'] = False
                try:
                    new['CVSS'] = cve['impact']['baseMetricV3']['cvssV3']['baseScore']
                    new['HasCVSS'] = True
                except:
                    # Guess it doesn't have a CVSS V3 base score
                    pass
                
                # There's no consistency in what the CVE applies to
                # So we go through some best effort logic to extract
                # First see if there's a cep23Uri
                try:
                    cpe23uri = cve['configurations']['nodes'][0]['cpe_match'][0]['cpe23Uri']
                    cpe23uri_components = cpe23uri.split(":")
                    new['Impacts'] = cpe23uri_components[4] + " " + cpe23uri_components[5]
                except:
                    # No cpe23Uri, moving on
                    description = cve['cve']['description']['description_data'][0]['value']
                    skip_words = ("the", "in", "an", "a")
                    words = description.split(' ')
                    if "An issue was discovered" in description:
                        new['Impacts'] = words[5] + " " + words[6]
                    elif words[0].lower() in skip_words:
                        new['Impacts'] = words[1] + " " + words[2] + " " + words[3] + " " + words[4] + " " + words[5]
                    else:
                        new['Impacts'] = words[0] + " " + words[1] + " " + words[2] + " " + words[3] + " " + words[4]

                current_news.append(new)

    
    return current_news



def get_xml_feed(url):
    session = requests.Session()
    # Avoid getting blocked by Reddit due to the default requests agent string. 
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3945.117 Safari/537.36'})
    resp = session.get(url)
    return xmltodict.parse(resp.text)

def add_rss_data(current_news, source, url, link_key="link"):
    try: 
        feed = get_xml_feed(url)
        for item in feed['rss']['channel']['item']:
            new = {}
            new['Source'] = source
            new['Title'] = item['title']
            new['Date'] = '{}'.format(parse(item['pubDate']))
            #new['Description'] = item['description']
            new['URL'] = item[link_key]
            current_news.append(new)
    except Exception as e: 
        print(e)
    return current_news

def add_rss_data_v2(current_news, source, url):
    feed = get_xml_feed(url)
    for entry in feed['feed']['entry']:
        new = {}
        new['Source'] = source
        if source.startswith('GA'):
            # Handles Google Alerts RSS title
            new['Title'] = entry['content']['#text']
        else:
            new['Title'] = entry['title']
        new['Date'] = '{}'.format(parse(entry['updated']))
        new['URL'] = entry['link']['@href']
        current_news.append(new)
    return current_news

# Create our lists
all_news = []
breach_news = []
tool_news = []
vuln_news = []

# Run through our news feed sources and add to all news
# Reddit 
# Note on Reddit requests: They're staggered to avoid hitting their rate limit when we make 2 requests within 6 seconds
all_news = add_rss_data_v2(all_news, 'reddit.com/r/InfoSecNews', "https://www.reddit.com/r/InfoSecNews.rss") 
# All news RSS feeds
all_news = add_rss_data_v2(all_news, 'GA:Security Breach', "https://www.google.com/alerts/feeds/14902217249725225541/1637945407231648777")
all_news = add_rss_data_v2(all_news, 'GA:Ransomware Attack', "https://www.google.com/alerts/feeds/14902217249725225541/253555712562062329")
all_news = add_rss_data_v2(all_news, 'GA:MageCart Attack', "https://www.google.com/alerts/feeds/14902217249725225541/2460322655362916407")
all_news = add_rss_data(all_news, 'SANS Internet Storm Center', "https://isc.sans.edu/rssfeed.xml")
all_news = add_rss_data(all_news, 'The Hacker News', "http://feeds.feedburner.com/TheHackersNews?format=rss", "feedburner:origLink")
all_news = add_rss_data(all_news, 'BleepingComputer', "https://www.bleepingcomputer.com/feed/")
all_news = add_rss_data(all_news, 'ITPro.', "https://www.itpro.co.uk/security/feed")
all_news = add_rss_data(all_news, 'Krebs On Security', "https://krebsonsecurity.com/feed/")
all_news = add_rss_data(all_news, 'Threatpost', "https://threatpost.com/feed/")
all_news = add_rss_data(all_news, 'Wired', "https://www.wired.com/feed/category/security/latest/rss")
all_news = add_rss_data_v2(all_news, 'reddit.com/r/devsecops', "https://www.reddit.com/r/devsecops.rss") 
all_news = add_rss_data(all_news, 'SecurityWeek', "https://feeds.feedburner.com/securityweek", "feedburner:origLink")
all_news = add_rss_data(all_news, 'Security Affairs', "https://securityaffairs.co/wordpress/feed")
all_news = add_rss_data(all_news, 'Naked Security', "https://nakedsecurity.sophos.com/feed/")
all_news = add_rss_data(all_news, 'KitPloit', "https://feeds.feedburner.com/PentestTools", "feedburner:origLink")
all_news = add_rss_data(all_news, 'Securelist', "https://securelist.com/feed/")
all_news = add_rss_data(all_news, 'Zero Day Initiative - Upcoming', "https://www.zerodayinitiative.com/rss/upcoming")
all_news = add_rss_data(all_news, 'Zero Day Initiative - Published', "https://www.zerodayinitiative.com/rss/published")
all_news = add_rss_data(all_news, 'Zero Day Initiative - Blog', "https://www.zerodayinitiative.com/blog?format=rss")
all_news = add_rss_data(all_news, 'Bitdefender Blog', "http://feeds.feedburner.com/BusinessInsightsInVirtualizationAndCloudSecurity", "feedburner:origLink")
all_news = add_rss_data_v2(all_news, 'reddit.com/r/netsec', "https://www.reddit.com/r/netsec.rss")
# Tool specific news
tool_news = add_rss_data(tool_news, 'Rapid7', 'https://blog.rapid7.com/rss/')
tool_news = add_rss_data(tool_news, 'KitPloit', "https://feeds.feedburner.com/PentestTools", "feedburner:origLink")
# Vuln specific news
vuln_news = add_cve_data(vuln_news)




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
    'All News': sort_uniq(all_news), 
    'Breach News': sort_uniq(breach_news), 
    'Tool News': sort_uniq(tool_news),
    'Vuln News': sort_uniq(vuln_news)
}
f = open("../../UI/v1/src/data.json", "w")
f.write(json.dumps(out))
f.close()

