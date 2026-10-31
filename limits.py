import json
import datetime

username = input("Enter username (user01, user02, user03): ")
# data ile elaqelendirme
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

if username not in data["accounts"]
    print("User not found.")
else:
    account = data["accounts"][username]
    today = str(datetime.date.today())
     # faylda saxlanan tarix bu gündürsə, saxlanan məbləği götürürük
    # başqa gündürsə (və ya heç nə yoxdursa), bu gün hələ pul yatırılmayıb
    if account.get("deposit_date") == today:
        deposited_today = account["deposited_today"]
    else:
        deposited_today = 0

    remaining_limit = 2000 - deposited_today

    print("Daily limits")
    print("Deposited today:", deposited_today, "/ 2000 AZN")
    print("Remaining deposit limit:", remaining_limit, "AZN")