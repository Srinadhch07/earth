import csv
from jobspy import scrape_jobs
jobs = scrape_jobs(
site_name=[
"indeed",
"linkedin",
"zip_recruiter",
"google",
],
search_term="software engineer",
google_search_term="software engineer jobs near Hyderabad since yesterday",
location="Hyderabad, Telangana, India",
results_wanted=20,
hours_old=72,
country_indeed="INDIA",
linkedin_fetch_description=True,
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
jobs.to_csv(
"jobs.csv",
quoting=csv.QUOTE_NONNUMERIC,
escapechar="\\",
index=False
)