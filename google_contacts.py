from os import read
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import datetime

email_acc = input('Provide your email address: ')
email_pass = input('Password: ')
wait_time = int(input('How many seconds do you need to finish 2FA: '))
total_contacts = int(input('How many contacts do you have: '))

scroll_number = int(total_contacts / 7.5 )

x = datetime.datetime.now()
hour = x.hour
minute = x.minute
date_1= x.day
month = x.month
year = x.year
date_time1 = f'{date_1}-{month}-{year}_{hour}-{minute}'
chrome_options  = Options()
chrome_path = which("chromedriver")
driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_options)

link = 'https://contacts.google.com/frequent?hl=en'
driver.get(link)
driver.maximize_window()
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
)
element.send_keys(f'{email_acc}')
driver.find_element_by_xpath("//*[@id='identifierNext']/div/button/div[2]").click()

sleep(2)
element1 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
)
element1.send_keys(f'{email_pass}')
driver.find_element_by_xpath("//*[@id='passwordNext']/div/button/div[2]").click()

# sleep(2)
try:
    element2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='yDmH0d']/div[4]/div/div[2]/span/div/div/div[2]/div[3]/div/div/button/span"))
    )
    element2.click()
except:
    pass
sleep(wait_time)

data = []
list = {}
try:
    for i in range(scroll_number):
        scroll = driver.find_element_by_xpath("//div[@class='XXcuqd'][9]/div/div[2]/span")
        for each in driver.find_elements_by_class_name("XXcuqd"):
            try:
                name = each.find_element_by_xpath(".//div/div[2]/span").text
            except:
                name = '-'
            try:
                email = each.find_element_by_xpath(".//div/div[3]/a").text
            except:
                email = '-'
            try:
                phone = each.find_element_by_xpath(".//div/div[4]/span").text
            except:
                phone = '-'
            try:
                job = each.find_element_by_xpath(".//div/div[5]").text
            except:
                job = '-' 
            print(name)   
            print(email)
            print(phone)
            print(f"{job}\n")
            list= {
                'Name':name,
                'Email': email,
                'Phone Number': phone,
                'Job Title & Company': job
            }
            data.append(list)
        for i in range(10):
            scroll.send_keys(Keys.ARROW_DOWN)
except:
    pass

print(len(data))
df1 = pd.DataFrame(data)
df = df1.drop_duplicates(subset=['Name'], keep='first').reset_index(drop=True)
df.to_csv(f'google_contacts_{date_time1}.csv',encoding='utf-8', index=False)