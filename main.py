import glassdoor_scraper as gs 

keyword = "data scientist"
num_jobs = 300
df = gs.get_jobs(keyword, num_jobs, verbose=False, verbose2=False, slp_time=3)
df.to_csv('glassdoor_jobs2.csv', index = False)
# verboses are for testing (can we collect the data properly or not, it prints it on the screen while collecting)
# If you're not testing, leave it as is.