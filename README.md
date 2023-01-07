# Race scheduler
Calculates training days based on race schedule and race day

Uses as input a csv file that contains details of training days for each week

Optionally creates entries in Google calendar. This requires some setup: see [this page](https://developers.google.com/calendar/api/quickstart/python) for details.

Run: `python race_scheduler.py <schedule.csv> <race_date_in_YYYY-MM-DD> <distance|time> [--create-entries <tag>]`