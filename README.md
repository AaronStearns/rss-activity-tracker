![RSS Logo](/rss_logo.jpeg =250x250)

# rss-activity-tracker

A dictionary keyed by company with values as lists of RSS feed urls can be found in companies_rss_dict.py

The file rss_activity_tracker.py imports this dict from companies_rss_dict.py

## To run:

1) Using the command line, navigate to the folder containing rss_activity_tracker.py and companies_rss_dict.py

3) Five args are passed to the script. The five args correspond to the range of days to check if a company has not had activity in that time. The format is:

[start_day] [start_month] [end_day] [end_month] [year]

In this example, the range being checked is December 1st to December 3rd, 2020 <br />
`>python rss_activity_tracker.py 1 12 3 12 2020`

And in this example, the range being checked is April 29th to May 3rd, 2018 <br />
`>python rss_activity_tracker.py 29 4 3 5 2018`

Currently, functionality is not in place for checking dates across a range of years. 
