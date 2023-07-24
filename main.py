import glassdoor_scraper as gs
import to_excel as ex

keyword = "data scientist"
num_jobs = 3
df = gs.get_jobs(keyword, num_jobs, verbose=False, verbose2=False, slp_time=5)
# verboses are for testing (can we collect the data properly or not, it prints it on the screen while collecting)
# If you're not testing, leave it as is.
