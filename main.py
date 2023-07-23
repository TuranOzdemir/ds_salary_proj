# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:08:58 2023

@author: TURAN
"""

import glassdoor_scraper as gs
#import pandas as pd

df = gs.get_jobs("data scientist", 35, False, False, 4)
 