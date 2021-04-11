from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import regex as re
from fantasticlibrary import PlayerAttributes as pa
from fantasticlibrary import secrets
import pandas as pd
import gspread
from fantasticlibrary import next_available_row as nr


driver = webdriver.Chrome('/Users/adriaferrer/IDIADA_Repos/Moneyball/01_get_data/chromedriver')

username = secrets.biwenger.username
password = secrets.biwenger.password

# Open the site and click to go to login
driver.get('https://biwenger.as.com/')
driver.find_element_by_css_selector('button').click()

# Login
driver.find_element_by_css_selector('input').send_keys(username + Keys.TAB + password + Keys.ENTER)

# Accept cookies
time.sleep(2)
driver.find_element_by_id('didomi-notice-agree-button').click()

# We get the soup for the page 1 players
soup = BeautifulSoup(driver.page_source, "lxml")

# Get all board posts
posts = soup.find_all("league-board-post")

all_moves = []
for post in posts:
    if "Mercado de fichajes" in str(post):
        id_time = str(post).find("time-relative")
        timestamp = str(post)[id_time + 40:725].split('"')[1]
        timed_market_post = [timestamp, post, "market"]
        all_moves.append(timed_market_post)

    elif "Fichajes" in str(post):
        id_time = str(post).find("time-relative")
        timestamp = str(post)[id_time + 40:725].split('"')[1]
        timed_market_post = [timestamp, post, "transfers"]
        all_moves.append(timed_market_post)

# Find each all movements in the current scroll

market_data = []

for move in all_moves:
    timestamp = move[0]
    all_player_cards = str(move[1]).split('player-card')[1::2]

    for player_card in all_player_cards:

        # Get player name
        name_player = pa.get_player_name(player_card)

        # Get transaction cost
        cost, id_trans = pa.get_transaction_cost(player_card)

        # Get buyer and seller
        buyer, seller = pa.get_buyer_seller(player_card, move, id_trans)

        # We create each row with the player name, the cost, the buyer and the seller
        movement_details = [name_player, cost, buyer, seller, timestamp]
        market_data.append(movement_details)

market_movements_df = pd.DataFrame(market_data)
market_movements_df.rename(columns={0: "player", 1: "cost", 2: "Buyer", 3: "Seller", 4: "timestamp"}, inplace=True)

# Upload data
gc = gspread.service_account(filename='/Users/adriaferrer/IDIADA_Repos/Moneyball/01_get_data/creds.json')
sh = gc.open("Market_data").sheet1

next_row = nr.next_available_row(sh)
last_row = len(market_movements_df.values.tolist()) + int(next_row)
sh.update(f'A{next_row}:E{last_row}', market_movements_df.values.tolist())

# Download and remove duplicates
raw_market_movements = pd.DataFrame(sh.get_all_values())
updated_market_movements = raw_market_movements.drop_duplicates()

# Upload clean data
sh2 = gc.open("Market_data_clean").sheet1
sh2.update([updated_market_movements.columns.values.tolist()] + updated_market_movements.values.tolist())

driver.quit()
