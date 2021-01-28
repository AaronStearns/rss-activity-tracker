import sys
import requests
import xmltodict
from datetime import datetime

##### Main dict #####
# URLs stored as lists in case a company has more than one rss url
rss_dict = { 
  "crime_junkie": { "rss_urls": ['https://feeds.megaphone.fm/ADL9840290619'] }, 
  "new_york_times": { "rss_urls": ['https://feeds.simplecast.com/54nAGcIl'] } ,
  "my_favorite_murder": { "rss_urls": ['https://www.omnycontent.com/d/playlist/aaea4e69-af51-495e-afc9-a9760146922b/44bbf446-4627-4f83-a7fd-ab070007db11/72b96aa8-88bd-480a-87af-ab070007db36/podcast.rss'] }
}

####################################################################################
##### Helper Methods #####
####################################################################################
def parse_rss_url_xml( company_and_rss_url_dict ):
  """
  Parses dates into dict with structure:
  {
    'company_name': { 'posts': 
                        { 2020: 
                          { 12: [21, 18, 14, 7, 4, 1], 
                            11: [30, 23, 16, 9, 2], 
                            ...
                          }
  }
  Where a given company contains post years, a given post year contains
  post months as keys, and a given post month contains a list of post days as ints  
  """  
  rss_published_days = {}

  for company in company_and_rss_url_dict:
    # Add company names to the dict
    if company not in rss_published_days:
      rss_published_days[company] = {}
      rss_published_days[company]['posts'] = {}

    for rss_url in company_and_rss_url_dict[company]['rss_urls']:
      response = requests.get(rss_url)
      rss_data_dict = xmltodict.parse(response.content)

      try:
        for value in rss_data_dict['rss']['channel']['item']: 
          rss_published_days = create_publish_history_dicts_for_RSS(value, company, rss_published_days)
      except:
        pass

  return rss_published_days


def create_publish_history_dicts_for_RSS( value, company, rss_published_days ):
  # The 'pubDate' (published date) node from the parsed XML
  date_string = value['pubDate']

  try:
    # Date format from rss 'pubDate': Mon, 25 Jan 2021 08:00:00 -0000
    date = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')

    if date.year not in rss_published_days[company]['posts']:
      rss_published_days[company]['posts'][date.year] = {}

    if date.month not in rss_published_days[company]['posts'][date.year]:
      rss_published_days[company]['posts'][date.year][date.month] = []
    
    if date.day not in rss_published_days[company]['posts'][date.year][date.month]:
      rss_published_days[company]['posts'][date.year][date.month].append(date.day)
  except:
    pass

  return rss_published_days

####################################################################################
##### Main Method #####
####################################################################################

def companyActivityTracker( start_day, start_month, start_year, end_day, end_month, end_year ):
  # Defining helpful error messages for using method
  general_method_error = "ERROR: companyActivityTracker() method \n"
  if start_month == end_month and start_day >= end_day:
    return general_method_error + "Start day is greater than or equal to end day."
  if start_month > end_month:
    return general_method_error + "Start month is greater than end month."
  if start_year > end_year:
    return general_method_error + "Start year is greater than end year."
  
  # Function to determine which companies had no activity for a given date range
  publish_dates_dict = parse_rss_url_xml(rss_dict)

  results_dict = {} # KEY: company VALUE: list of post dats between range start_day and end_day 

  for company in publish_dates_dict:
    if company not in results_dict:
      results_dict[company] = []

    if start_year == end_year and start_year in publish_dates_dict[company]['posts']:
      # checking a date range within the same month of the same year
      if start_month == end_month and start_month in publish_dates_dict[company]['posts'][start_year]:
        for day in publish_dates_dict[company]['posts'][start_year][start_month]:
          if day <= end_day and day >= start_day:
            results_dict[company].append(day)
          """
      elif start_month < end_month and start_month in publish_dates_dict[company]['posts'][start_year]:
        if end_month in publish_dates_dict[company]['posts'][start_year]:
          for day in publish_dates_dict[company]['posts'][start_year][start_month]:
            if day >= start_day:
              results_dict[company].append(day)
          """
          #TODO: check across months


  comapnies_without_activity = []
  for company in results_dict:
    if len(results_dict[company]) == 0:
      comapnies_without_activity.append(company)

  return comapnies_without_activity


print(companyActivityTracker(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])))


