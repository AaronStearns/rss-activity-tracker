import requests
import xmltodict


url = "https://feeds.megaphone.fm/ADL9840290619"
response = requests.get(url)
data = xmltodict.parse(response.content)

most_recent_published = []
for i, key in enumerate(data['rss']['channel']['item']): 
  if i == 0:
    most_recent_published.append(key['pubDate'])

print(most_recent_published)



# read each rss url

# convert the XML to a dict 
# save only the <item> nodes and their <time> subnodes that have the rss upload time

# use regex to parse the item time into a formatted timestamp

# ??? create python class Company with properties: Name, Urls, DaysSincePosting



