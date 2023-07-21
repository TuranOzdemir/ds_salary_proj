from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service


def extract_company_name(full_name):
    if ' ' in full_name:
        return full_name[:full_name.rindex(' ')]
    return full_name

def get_jobs(keyword, num_jobs, verbose,verbose2, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    service = Service(executable_path='/Users/TURAN\Documents/ds_salary_proj/chromedriver.exe')
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(service = service, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            element = driver.find_element(By.CLASS_NAME, "selected")
            element.click()
        except ElementClickInterceptedException:
            pass

        time.sleep(slp_time)

        try:
            # Wait for the button to be clickable (optional but recommended).
            wait = WebDriverWait(driver, 5)  # Wait for up to 10 seconds.
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "e1jbctw80")))
            #driver.find_element(By.CLASS_NAME, "e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40").click()  #clicking to the X.
            button.click()
        except NoSuchElementException:
            pass

        
        #Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(5)
            collected_successfully = False
            
            while not collected_successfully:
                
                try:
                    company_name_full = driver.find_element(By.CSS_SELECTOR ,'[data-test="employerName"]').text
                    company_name = extract_company_name(company_name_full)
                except:
                    print("company_name is a problem")
                    pass
                try:    
                    location = driver.find_element(By.CSS_SELECTOR,'[data-test="location"]').text
                except:
                    print("location is a problem")
                    pass
                try:
                    # Wait for the job title element to be present and visible
                    job_title_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="jobTitle"]'))
                    )
                    job_title = job_title_element.text
                    #print("Job Title: {}".format(job_title))
                except TimeoutException:
                    print("Job title element took too long to load.")
                    job_title = "N/A"  # Provide a default value in case the job title is not found
                except NoSuchElementException:
                    print("Job title element not found.")
                    job_title = "N/A"  # Provide a default value in case the job title element is not found
                except:
                    print("job_title is a problem")
                    print(traceback.format_exc())
                    job_title = "N/A"  # Provide a default value in case of any other issue
                # try:
                #     job_description = driver.find_element(By.CSS_SELECTOR, '.jobDescriptionContent.desc').text
                # except:
                #       print("job_description is a problem")
                #       pass
                collected_successfully = True
              

            try:
                salary_estimate = driver.find_element(By.CLASS_NAME, 'css-1xe2xww.e1wijj242').text.split(':')[-1].strip()
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element(By.CSS_SELECTOR,'[data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                
                #print("Job Title: {}".format(job_title))
                #print("Salary Estimate: {}".format(salary_estimate))
                #print("Job Description: {}".format(job_description[:500]))
                #print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                #print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element(By.XPATH,'.//div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    size = driver.find_element('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

                
            if verbose2:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH,'.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
#This line will open a new chrome window and start the scraping.
