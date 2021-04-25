from colorama import init, Fore, Back, Style
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
from bs4 import BeautifulSoup
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
import random
import datetime
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


email_acc = input('Provide your email address: ')
email_pass = input('Password: ')
wait_time = int(input('How many seconds do you need to finish 2FA: '))
total_contacts = int(input('How many contacts do you have: '))
scroll_number = int(total_contacts / 6) + 1

x = datetime.datetime.now()
hour = x.hour
minute = x.minute
date_1= x.day
month = x.month
year = x.year
date_time1 = f'{date_1}-{month}-{year}_{hour}-{minute}'
options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    
user_agent = 'FC'
options.add_argument(f"user-agent={user_agent}")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# chrome_path = which("chromedriver")
driver = webdriver.Chrome( options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
        

# time.sleep(3)
driver.maximize_window()
driver.get('https://accounts.google.com/servicelogin')
time.sleep(2)
driver.find_element_by_id('Email').send_keys(email_acc)
time.sleep(0.5)
driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/form/div/div/input').click()
time.sleep(0.5)
driver.find_element_by_id('password').send_keys(email_pass)
driver.find_element_by_id('submit').click()
sleep(wait_time)
link = 'https://contacts.google.com/frequent?hl=en'
driver.get(link)
try:
    element2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='yDmH0d']/div[4]/div/div[2]/span/div/div/div[2]/div[3]/div/div/button/span"))
    )
    element2.click()
except:
    pass

data = []
list = {}
try:
    for i in range(scroll_number):
        scroll = driver.find_element_by_xpath("//div[@class='XXcuqd'][10]/div/div[2]/span")
        soup = BeautifulSoup(driver.page_source,'html.parser')
        for each in soup.findAll('div',attrs = {'class':'XXcuqd'}):
            try:
                name = each.find('span').get_text()
            except:
                name = '-'
            try:
                email = each.find('a').get_text()
            except:
                email = '-'
            try:
                phone = each.findAll('span')[1].get_text()
            except:
                phone = '-'
            try:
                job = each.find('div',attrs = {'class':'E6Tb7b ZAFZMe'}).get_text()
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
        for i in range(8):
            scroll.send_keys(Keys.ARROW_DOWN)
except:
    pass

# print(len(data))
df1 = pd.DataFrame(data)
df = df1.drop_duplicates(subset=['Name'], keep='first').reset_index(drop=True)
df.to_csv(f'google_contacts_{date_time1}.csv',encoding='utf-8', index=False)