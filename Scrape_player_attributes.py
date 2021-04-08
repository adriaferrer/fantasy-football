from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from fantasticlibrary import secrets
from fantasticlibrary import PlayerAttributes as pa
from fantasticlibrary import next_available_row as nr
import pandas as pd
import datetime as dt
import gspread

driver = webdriver.Chrome('/Users/adriaferrer/Private_Repos/Fantasy_Football/fantasy-football/chromedriver')

username = secrets.biwenger.username
password = secrets.biwenger.password

# Open the site and click to go to login
driver.get('https://biwenger.as.com/players')
driver.find_element_by_css_selector('button').click()

# Login
driver.find_element_by_css_selector('input').send_keys(username + Keys.TAB + password + Keys.ENTER)

# Accept cookies
time.sleep(2)
driver.find_element_by_id('didomi-notice-agree-button').click()

# Create a list to save all the player attributes
player_attributes = []

# We collect the data for all the pages of the website
for page in range(58):

    # Get all the player cards for this page
    soup = BeautifulSoup(driver.page_source, "lxml")
    all_players = soup.find_all('player-card')

    # Get the attributes for each player
    for player in all_players:
        player_attributes.append(pa.PlayerAttributes(str(player)))

    # Go to next page
    try:
        driver.find_element_by_css_selector(
            'body > app-root > main > div > ng-component:nth-child(3) > div > div > player-list > adv-list > div.filters.footer.ng-star-inserted > pagination > ul > li:nth-child(8)').click()
    except:
        break

# Create df with all the collected data, adding timestamp
df_player_att = pd.DataFrame(player_attributes)
df_player_att.rename(columns={0: 'player', 1: 'team', 2: 'value', 3: 'points'}, inplace=True)
df_player_att['timestamp'] = dt.datetime.now()
df_player_att['timestamp'] = df_player_att['timestamp'].astype(str)

# Upload data to gsheets
gc = gspread.service_account(filename='/Users/adriaferrer/IDIADA_Repos/Moneyball/01_get_data/creds.json')
sh = gc.open("Players_data").sheet1

next_row = nr.next_available_row(sh)
last_row = len(df_player_att.values.tolist()) + int(next_row)
sh.update(f'A{next_row}:E{last_row}', df_player_att.values.tolist())

driver.quit()
