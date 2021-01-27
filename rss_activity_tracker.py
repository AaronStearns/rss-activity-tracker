import requests
import xmltodict
from datetime import datetime

# URLs stored as lists in case a company has more than one rss url
rss_dict = { 
  "crime_junkie": { "rss_urls": ['https://feeds.megaphone.fm/ADL9840290619'] }, 
  "new_york_times": { "rss_urls": ['https://feeds.simplecast.com/54nAGcIl'] } 
}

def calculateDaysSinceLastPublish(company_and_rss_url_dict):

  # Dict to store results in format:
  # KEY: Company (string)
  # VALUE: List of days that rss published
  rss_published_days = {}

  #today = datetime.now().astimezone()

  for company in company_and_rss_url_dict:

    if company not in rss_published_days:
      rss_published_days[company] = {}

    for rss_url in company_and_rss_url_dict[company]['rss_urls']:
      
      response = requests.get(rss_url)
      rss_data_dict = xmltodict.parse(response.content)

      try:
        for key in rss_data_dict['rss']['channel']['item']: 
          rss_published_days = createPublishHistoryDictsForRSS(key, company, rss_published_days)
      except:
        pass

  return rss_published_days


def createPublishHistoryDictsForRSS(key, company, rss_published_days):
  """
  Parses dates into dict with structure:
  {
    'company_name': { 2020: 
                      { 12: [21, 18, 14, 7, 4, 1], 
                        11: [30, 23, 16, 9, 2], 
                        ...
                    }
  }
  Where a given company contains posts years, and post years containing
  post months as keys and post days as ints in a list for corresponding months 
  """  

  date_str = key['pubDate']

  try:
    # Date format from rss 'pubDate': Mon, 25 Jan 2021 08:00:00 -0000
    date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    
    if date.year not in rss_published_days[company]:
      rss_published_days[company][date.year] = {}

    if date.month not in rss_published_days[company][date.year]:
      rss_published_days[company][date.year][date.month] = []
    
    if date.day not in rss_published_days[company][date.year][date.month]:
      rss_published_days[company][date.year][date.month].append(date.day)
  except:
    pass

  return rss_published_days

print(calculateDaysSinceLastPublish(rss_dict))


