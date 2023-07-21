# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:08:58 2023

@author: TURAN
"""

import glassdoor_scraper as gs
import pandas as pd

df = gs.get_jobs("data scientist", 15,True, False, 5)
    
# company name + (rating ile birlikte geliyor ayırmak lazım)
# Job Title - (ne yaparsam yapıyım boş geliyor) 
# salary estimate + 
# Location +
# Rating +
# description -

# geri kalan : (henüz hiç bakmadım)
# Size: -1
# Founded: -1
# Type of Ownership: -1
# Industry: -1
# Sector: -1
# Revenue: -1
# Competitors: -1 