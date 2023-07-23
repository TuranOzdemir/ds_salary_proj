# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:08:58 2023

@author: TURAN
"""

import glassdoor_scraper as gs
#import pandas as pd

df = gs.get_jobs("data scientist", 35, False, False, 4)
    
# company name + (rating ile birlikte geliyor ayırmak lazım data cleaning bölümünde ayrılacak)
# Job Title +
# salary estimate + 
# Location +
# Rating +
# description + (liste halinde tek sayfadan aldım burda bir ihtimal sorun çıkabilir görücez)

# geri kalan : 
# Size: +
# Founded: -1
# Type of Ownership: -1
# Industry: -1
# Sector: -1
# Revenue: -1
# Competitors: -1 

#   File ~\Documents\ds_salary_proj\glassdoor_scraper.py:135 in get_jobs
#     industry = overview[3].find_element(By.CLASS_NAME, 'css-i9gxme.e1pvx6aw2').text

# IndexError: list index out of range
# bazı iş ilanlarında company overview farklı 
# Size
# Founded
# Type of Ownership
# Industry
# Sector
# Revenue
# Competitors 
# bunların hepsi olmayabiliyor 
# overview = driver.find_elements(By.CLASS_NAME, 'd-flex.justify-content-start.css-rmzuhb.e1pvx6aw0')
# overview liste olarak alınıyor ve her bir elemente listeler üzerinden ulaşılıyor 
# ama eksik olduğunda overview[5] olarak aldığım değer "list index out of range" hatası veriyor.
