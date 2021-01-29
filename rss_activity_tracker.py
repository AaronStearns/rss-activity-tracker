import sys
import requests
import xmltodict
from datetime import datetime
from companies_rss_dict import rss_dict # Main dict of companies and their rss urls

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
    # add company names to the dict
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


def check_sys_args():
  publish_dates_dict = parse_rss_url_xml(rss_dict)

  # make sure that day, month, and year sys.argv args fall within these ranges
  month = range(1,13) # 1-12, 13 not inclusive
  day = range(1,32)
  rss_post_years = set()

  for company in publish_dates_dict:
    for year in publish_dates_dict[company]['posts']:
      rss_post_years.add(year)
  try:
    if int(sys.argv[1]) and int(sys.argv[3]) not in day:
      return "ERROR: Day values do not fall within the range 1-31"
    if int(sys.argv[2]) and int(sys.argv[4]) not in month:
      return "ERROR: Month values do not fall within the range 1-12"
    if int(sys.argv[5]) not in rss_post_years:
      return "ERROR: Year value do not fall within the rss post year range"
  except:
    pass

  return publish_dates_dict


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

####################################################################################
##### Main Methods #####
####################################################################################
def companyActivityTracker( start_day, start_month, end_day, end_month, year ):
  # Defining helpful error messages for using method
  general_method_error = "ERROR: companyActivityTracker() method \n"
  if start_month == end_month and start_day >= end_day:
    return general_method_error + "Start day is greater than or equal to end day."
  if start_month > end_month:
    return general_method_error + "Start month is greater than end month."
  
  # Function to determine which companies had no activity for a given date range
  publish_dates_dict = check_sys_args()

  if isinstance(publish_dates_dict, dict):
    pass
  else:
    return publish_dates_dict # will print helpful error message

  results_dict = {} # KEY: company VALUE: list of post dats between range start_day and end_day 

  for company in publish_dates_dict:
    if company not in results_dict:
      results_dict[company] = []

    if year in publish_dates_dict[company]['posts']:
      # checking a date range within the same month of the same year
      if start_month == end_month and start_month in publish_dates_dict[company]['posts'][year]:
        for day in publish_dates_dict[company]['posts'][year][start_month]:
          if day <= end_day and day >= start_day:
            results_dict[company].append(day)
      

      elif start_month < end_month and start_month in publish_dates_dict[company]['posts'][year] and end_month in publish_dates_dict[company]['posts'][year]:
        for month in range(start_month, end_month+1):
          if month not in publish_dates_dict[company]['posts'][year]:
            continue # no posts for that month, nothing to append to results_dict
          else:
            if month == start_month:
              for day in publish_dates_dict[company]['posts'][year][start_month]:
                if day >= start_day:
                  results_dict[company].append(day)
            elif month == end_month:
              for day in publish_dates_dict[company]['posts'][year][end_month]:
                if day <= end_day:
                  results_dict[company].append(day)
            else:
              for day in publish_dates_dict[company]['posts'][year][month]:
                results_dict[company].append(day) # append all posts in the month to results_dict

  comapnies_without_activity = []
  for company in results_dict:
    if len(results_dict[company]) == 0: # no posts for a given company
      comapnies_without_activity.append(company)

  return comapnies_without_activity

def check_args_and_call_companyActivityTracker():
  # check that all args are indeed int values
  flag = 0
  for i in range(1, len(sys.argv)):
    if intTryParse(sys.argv[i])[1] == False:
      flag = 1

  if len(sys.argv) != 6:
      print("ERROR: Incorrect number of args given")
  elif len(sys.argv) == 6 and flag == 0:
    print(companyActivityTracker(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])))
  else:
    print("ERROR: Non-integer value passed as date")
  return

check_args_and_call_companyActivityTracker()