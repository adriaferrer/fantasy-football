import pandas as pd
import gspread
import datetime as dt

# Get the data
gc = gspread.service_account(filename='/Users/adriaferrer/Private_Repos/Fantasy_Football/fantasy-football/creds.json')
sh = gc.open("Managers_balance").sheet1
balance = pd.DataFrame(sh.get_all_values(), columns=["Manager", "balance"]).drop([0])
managers = list(balance["Manager"])
values = list(balance["balance"])
values = map(int, values)

sh2 = gc.open("Market_data_clean").sheet1
column_names = ["player", "cost", "buyer", "seller", "timestamp"]
transactions = pd.DataFrame(sh2.get_all_values(), columns=column_names).drop([0, 1])
transactions["cost"] = transactions["cost"].astype(int)
transactions.replace(to_replace="mercado", value="market", inplace=True,)

# Create ledger
# Get current balance
ledger = dict.fromkeys(managers, 0)
ledger.update(zip(ledger, values))

# Update ledger
for index, row in transactions.iterrows():
    if row["buyer"] != "market":
        ledger[row["buyer"]] -= row["cost"]
    else:
        pass

    if row["seller"] != "market":
        ledger[row["seller"]] += row["cost"]
    else:
        pass

# Upload final balance
sh.update("B2:B10", pd.DataFrame.from_dict(ledger, orient='index').values.tolist())
sh.update("B1", str(dt.datetime.now().replace(microsecond=0)))
