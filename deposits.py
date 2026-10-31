import json
import datetime 
username = input("Enter username, example: user01, user02, user03 :")
with open("data.json", "r", encoding="utf-8") as fayl:
    data = json.load(fayl)

if username not in data["accounts"]:
    print("User not found.")
else:
    hesab = data["accounts"][username]
    print("Balance:", hesab["balance"], "AZN")
