from helper_methods.parse_rss_urls_xml import parse_rss_urls_xml
from typing import List, Dict



def company_activity_tracker( start_day: int, start_month: int, end_day: int, end_month: int, year: int) -> List[str]:
  publish_dates: Dict = parse_rss_urls_xml()

  # KEY: company VALUE: list of post dats between range start_day and end_day 
  results: Dict = {} 

  for company in publish_dates:
    if company not in results:
      results[company] = []

    if year in publish_dates[company]['posts']:
      # Checking a date range within the same month of the same year
      if start_month == end_month and start_month in publish_dates[company]['posts'][year]:
        for day in publish_dates[company]['posts'][year][start_month]:
          if day <= end_day and day >= start_day:
            results[company].append(day)
      
      elif start_month < end_month and start_month in publish_dates[company]['posts'][year] and end_month in publish_dates[company]['posts'][year]:
        for month in range(start_month, end_month+1):
          if month not in publish_dates[company]['posts'][year]:
            continue # No posts for that month, nothing to append to results
          else:
            if month == start_month:
              for day in publish_dates[company]['posts'][year][start_month]:
                if day >= start_day:
                  results[company].append(day)
            elif month == end_month:
              for day in publish_dates[company]['posts'][year][end_month]:
                if day <= end_day:
                  results[company].append(day)
            else:
              for day in publish_dates[company]['posts'][year][month]:
                results[company].append(day) # Append all posts in the month to results

  compnies_without_activity: List[str] = []
  
  for company in results:
    if len(results[company]) == 0: # No posts for a given company
      compnies_without_activity.append(company)

  return compnies_without_activity