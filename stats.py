'''
This file is intended to do the following types of work:
* download data from APIs
* screenscrape data from websites
* reduce the size of large datasets to something more manageable
* clean data: reducing/renaming columns, normalizing strings,
* generate data through relatively complicated calculations

To reduce processing time and to establish a "milestone", you should
save your processed data into the folder 'data_organized'.
You can do this with:
   df.to_csv('data_organized/filename.csv')

You may have helper files. But, this file should be the entry point.

You should test this file's code in `run_tests.py`. 
'''
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def main():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service, options = options)
    
    url = 'https://www.nba.com/players'

    driver.get(url)
    # label_element = driver.find_element(By.CLASS_NAME, "Toggle_toggle__2_SBA PlayerList_toggle__RL_YD")
    time.sleep(5)
    history_btn = driver.find_elements(By.CLASS_NAME, "Toggle_input__4dsrR")
    
    history_btn[0].click()
    time.sleep(5)
    
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    players = doc.find("tbody").find_all('tr')

    data = [{'Name': name_find(p), 'Team': team_find(p), 'CoI': coi_find(p)} for p in players]
    data = pd.DataFrame(data)
    
    print(data)

def name_find(player):
    n = player.find('div', class_='RosterRow_playerName__G28lg').find_all('p')
    return n[0].text + ' ' + n[1].text

def team_find(player):
    t = player.find('a', class_='Anchor_anchor__cSc3P RosterRow_team__AunTP')
    return t.text if t is not None else 'NONE'

def coi_find(player):
    return player.find_all('td', class_='text')[5].text
            
    

if __name__ == '__main__':
    main()
