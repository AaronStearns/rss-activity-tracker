![RSS Logo](/rss_logo.png)

# rss-activity-tracker

This is a script that takes in a dictionary of RSS feed urls to determine which RSS feed has not had any activity within a provided range of dates.

## Files:

`companies_rss_dict.py` contains a dictionary keyed by company with values as lists of RSS feed urls

`rss_activity_tracker.py` is the main script and imports the dict from `companies_rss_dict.py`

## To run:

1) Using the command line, navigate to the folder containing `rss_activity_tracker.py` and `companies_rss_dict.py`

3) Five args are passed to the script. The five args correspond to the range of days and months to check if a company has not had activity in that time. The format is:

[start_day] [start_month] [end_day] [end_month] [year]

In this example, the range being checked is December 1st to December 3rd, 2020 <br />
`>python rss_activity_tracker.py 1 12 3 12 2020`

And in this example, the range being checked is April 29th to May 3rd, 2018 <br />
`>python rss_activity_tracker.py 29 4 3 5 2018`

Currently, functionality is not in place for checking dates across a range of years. 
