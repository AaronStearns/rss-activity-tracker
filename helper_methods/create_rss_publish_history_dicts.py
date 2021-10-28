from datetime import datetime

def create_rss_publish_history_dicts( value, company, rss_published_days ):
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