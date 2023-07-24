# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:08:58 2023

@author: TURAN
"""

import glassdoor_scraper as gs
import to_excel as ex

keyword = "data scientist"
num_jobs = 3
df = gs.get_jobs(keyword, num_jobs, verbose=False, verbose2=False, slp_time=5)
