import requests
import xmltodict

"""
rss_dict = { 
  "crime_junkie": { "rss_urls": ['https://feeds.megaphone.fm/ADL9840290619', 'https://feeds.megaphone.fm/ADL9840290619'] }, 
  "new_york_times": { "rss_urls": ['https://feeds.simplecast.com/54nAGcIl'] } }

for key in rss_dict:
  for rss_url in rss_dict[key]['rss_urls']:
    print(rss_url)

"""

url = "https://feeds.megaphone.fm/ADL9840290619"
response = requests.get(url)
data = xmltodict.parse(response.content)

most_recent_published = []
try:
  for i, key in enumerate(data['rss']['channel']['item']): 
    if i == 0:
      most_recent_published.append(key['pubDate'])

  print(most_recent_published[0])
except:
  # move to next company key in rss_dict
  print("nah")



# read each rss url

# convert the XML to a dict 
# save only the <item> nodes and their <time> subnodes that have the rss upload time

# use regex to parse the item time into a formatted timestamp

# ??? create python class Company with properties: Name, Urls, DaysSincePosting



