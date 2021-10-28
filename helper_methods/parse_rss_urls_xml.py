from helper_methods.create_rss_publish_history_dicts import create_rss_publish_history_dicts
import requests
import xmltodict
from companies_rss_dict import rss_dict # Main dict of companies and their rss urls
from typing import Dict


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
def parse_rss_urls_xml() -> Dict:
  rss_published_days: Dict = {}

  for company in rss_dict:
    # Add company names to the dict
    if company not in rss_published_days:
      rss_published_days[company] = {}
      rss_published_days[company]['posts'] = {}

    for rss_url in rss_dict[company]['rss_urls']:
      response = requests.get(rss_url)
      rss_data: Dict = xmltodict.parse(response.content)

      try:
        for value in rss_data['rss']['channel']['item']: 
          rss_published_days = create_rss_publish_history_dicts(value, company, rss_published_days)
      except:
        pass

  return rss_published_days
