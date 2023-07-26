# ToDo List:
# Remove all the missing salary +
# salary parsing +
# company name text only +
# state field + and remote jobs +
# age of company (in progress) +
# parsing of job description (python etc.) +


import pandas as pd 
df = pd.read_csv('glassdoor_jobs_merged.csv')

# SALARY PARSING:
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

df = df[df['Salary Estimate'] != '-1'] # 213 adet -1 çıktı :0 kalan data 587 adet

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])# apply yazılan fonksiyonu df ye uygulamak için kullanılıyor
minus_kd = salary.apply(lambda x: x.replace('K','').replace('$', ''))

min_hr = minus_kd.apply(lambda x: x.lower().replace('per hour', ''))
df['min_salary'] = min_hr.apply(lambda x: x.split(' - ')[0]).astype(float)

df['max_salary'] = min_hr.apply(lambda x: x.split(' - ')[1] if ' - ' in x else -1).astype(float)

# Define a lambda function to calculate the average salary
avg = lambda x: (x['min_salary'] + x['max_salary']) / 2 if x['max_salary'] != -1 else x['min_salary']
df['avg_salary'] = df.apply(avg, axis=1)

# COMPANY NAME TEXT ONLY:

df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 
                             else x['Company Name'][:-3], axis = 1)


# STATE FIELD:

df.loc[df['Location'] == 'California', 'Location'] = 'California, US'
    
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1] if ',' in x else -1)
# look = df[['Location', 'job_state']]
df['remote_jobs'] = df['Location'].apply(lambda x: 1 if 'remote' in x.lower() else 0)
# If you want to see how many job applications there are in which city, uncomment below.
# df.job_state.value_counts()



# AGE OF COMPANY:

df['age'] = df.Founded.apply(lambda x: x if x < 0 else 2023 - x)


# PARSING OF JOB DESCRIPTION (PYTHON ETC.)
# python:
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

# R Studio: 
# df['R'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
# (Cant find any even if there is one because its just one letter and other patterns like 'r studio' or 'r-studio' did not exist in dataframe)

# spark:
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)

# AWS : (only 1 aws in df) +++++++ is it in or out ????
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() or 'amazon web services' in x.lower() else 0)

# excel:
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)


# SQL
df['sql'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)

# Tableau:
df['Tableau'] = df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)


df.to_csv('salary_data_cleaned.csv', index = False)





