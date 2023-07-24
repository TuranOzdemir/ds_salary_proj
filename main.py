import glassdoor_scraper as gs
import to_excel as ex

keyword = "data scientist"
num_jobs = 3
df = gs.get_jobs(keyword, num_jobs, verbose=False, verbose2=False, slp_time=5)
