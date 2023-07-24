# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:23:49 2023

@author: TURAN
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:53:50 2023

@author: TURAN
"""
import time
#import os
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.chrome.service import Service


def get_jobs(keyword, num_jobs, verbose=False, verbose2=False, slp_time=4):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()
    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    service = Service(executable_path='/Users/TURAN\Documents/ds_salary_proj/chromedriver.exe')
    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    url = f'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="{keyword}"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []
    def extract_job_details(job_button):
        job_button.click()
        time.sleep(5)
        collected_successfully = False
        check = None
        try:
            check = driver.find_element(By.CSS_SELECTOR, '.css-1cci78o')            
        except NoSuchElementException:
            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.CSS_SELECTOR, '[data-test="employerName"]').text
                    location = driver.find_element(By.CSS_SELECTOR, '[data-test="location"]').text
                    job_title = driver.find_element(By.CLASS_NAME, 'css-1vg6q84.e1tk4kwz4').text
                    job_description = driver.find_element(By.CLASS_NAME, 'jobDescriptionContent').text
                    collected_successfully = True
                except NoSuchElementException:
                    pass

            try:
                salary_estimate = driver.find_element(By.CLASS_NAME, 'css-1xe2xww.e1wijj242').text.split(':')[-1].strip()
            except NoSuchElementException:
                salary_estimate = -1

            try:
                rating = driver.find_element(By.CSS_SELECTOR, '[data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1

            try:
                overview = driver.find_elements(By.CLASS_NAME, 'd-flex.justify-content-start.css-rmzuhb.e1pvx6aw0')
                info_dict = {}
                for element in overview:
                    try:
                        category = element.find_element(By.CLASS_NAME, 'css-1taruhi.e1pvx6aw1').text
                        value = element.find_element(By.CLASS_NAME, 'css-i9gxme.e1pvx6aw2').text
                        info_dict[category] = value
                    except NoSuchElementException:
                        pass

                size = info_dict.get("Size", -1)
                founded = info_dict.get("Founded", -1)
                type_of_ownership = info_dict.get("Type", -1)
                industry = info_dict.get("Industry", -1)
                sector = info_dict.get("Sector", -1)
                revenue = info_dict.get("Revenue", -1)

            except NoSuchElementException:
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            if verbose2:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))

            jobs.append({
                "Job Title": job_title,
                "Salary Estimate": salary_estimate,
                "Rating": rating,
                "Company Name": company_name,
                "Location": location,
                "Job Description": job_description,
                "Size": size,
                "Founded": founded,
                "Type of ownership": type_of_ownership,
                "Industry": industry,
                "Sector": sector,
                "Revenue": revenue
            })
            return check

    while len(jobs) < num_jobs:
        try:
            element = driver.find_element(By.CLASS_NAME, "selected")
            element.click()
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException !!!!!!!")

        time.sleep(slp_time)
        wait = WebDriverWait(driver, 10)
        try:
            button = driver.find_element(By.CLASS_NAME, "e1jbctw80")
            if button:
                button.click()
            else:
                pass
        except (NoSuchElementException, ElementClickInterceptedException):
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "react-job-listing")
        for job_button in job_buttons:
            print("Progress: {}/{}".format(len(jobs), num_jobs))
            if len(jobs) >= num_jobs:
                break

            check = extract_job_details(job_button)
            if  check:
                continue
                

        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']")))
            # Click the button
            button.click()
            #driver.find_element(By.CLASS_NAME, 'navIcon.e13qs2070.job-search-4iku5v.e7xsrz90').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching the target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

        try:
            check = driver.find_element(By.CSS_SELECTOR, '.css-1cci78o').text
            print(check)
        except NoSuchElementException:
            pass
        else:
            print("Error Loading encountered. Skipping to the next job.")
            continue

    driver.quit()
    return pd.DataFrame(jobs)

