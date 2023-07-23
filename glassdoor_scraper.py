from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service



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
            print("ElementClickInterceptedException !!!!!!!")
            pass

        time.sleep(slp_time)
        wait = WebDriverWait(driver, 10)  # Wait for up to 5 seconds.
        try:
            # Wait for the button to be clickable (optional but recommended).
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "e1jbctw80")))
            #driver.find_element(By.CLASS_NAME, "e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40").click()  #clicking to the X.
            button.click()
        except (NoSuchElementException, ElementClickInterceptedException):
            pass

        i=0
        #Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  
            
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(5)
            collected_successfully = False
            
            try:
                check = driver.find_element(By.CSS_SELECTOR, '.css-1cci78o')
                continue
            except NoSuchElementException:
                while not collected_successfully:     
                    try:
                        try:
                            company_name = driver.find_element(By.CSS_SELECTOR ,'[data-test="employerName"]').text
                        except:
                            print("company_name is a problem")
                            pass
                        try:    
                            location = driver.find_element(By.CSS_SELECTOR,'[data-test="location"]').text
                        except:
                            print("location is a problem")
                            pass
                        try:
                            job_title = driver.find_element(By.CLASS_NAME, 'css-1vg6q84.e1tk4kwz4').text
                        except:
                            print("job_title is a problem")
                            pass
                        try:
                             job_description = driver.find_elements(By.XPATH, './/div[@class="mt-xxsm job-search-cw9jmf"]')[i].text
                        except:
                               print("job_description is a problem")
                               pass
                        collected_successfully = True
                    except:
                        #print("Error Loading. Skipping this job.")
                        #collected_successfully = True  # Bu işte hata olduğu için başarılı olarak kabul edip sonraki işe geçin.
                        pass
    
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
                    
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))
    
                try:
                    #Going to the Company Overview
                    overview = driver.find_elements(By.CLASS_NAME, 'd-flex.justify-content-start.css-rmzuhb.e1pvx6aw0')
                    
                    
                    # Create a dictionary to store the extracted information
                    info_dict = {}
                    
                    for element in overview:
                        try:
                            category = element.find_element(By.CLASS_NAME, 'css-1taruhi.e1pvx6aw1').text
                            value = element.find_element(By.CLASS_NAME, 'css-i9gxme.e1pvx6aw2').text
                            info_dict[category] = value
                        except NoSuchElementException:
                            # Handle the missing element (optional)
                            pass
                    
                    # Access the extracted information
                    size = info_dict.get("Size", -1)
                    founded = info_dict.get("Founded", -1)
                    type_of_ownership = info_dict.get("Type", -1)
                    industry = info_dict.get("Industry", -1)
                    sector = info_dict.get("Sector", -1)
                    revenue = info_dict.get("Revenue", -1)
                    
                    # You can access other fields in a similar way if needed
    
    
                except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1
    
                    
                if verbose2:
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    # print("Type of Ownership: {}".format(type_of_ownership))
                    # print("Industry: {}".format(industry))
                    # print("Sector: {}".format(sector))
                    # print("Revenue: {}".format(revenue))
                    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    
                jobs.append({"Job Title" : job_title,
                "Salary Estimate" : salary_estimate,
                "Rating" : rating,
                "Company Name" : company_name,
                "Location" : location,
                "Job Description" : job_description,
                "Size" : size,
                "Founded" : founded,
                "Type of ownership" : type_of_ownership,
                "Industry" : industry,
                "Sector" : sector,
                "Revenue" : revenue})
                #add job to jobs
                i+=1
        #Clicking on the "next page" button
        try:
            driver.find_element(By.CLASS_NAME,'navIcon.e13qs2070.job-search-4iku5v.e7xsrz90').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
        
        try:
            check = driver.find_element(By.CSS_SELECTOR, '.css-1cci78o').text
            print(check)
        except NoSuchElementException:
            pass
        else:
            print("Error Loading encountered. Skipping to the next job.")
            continue
    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
#This line will open a new chrome window and start the scraping.
