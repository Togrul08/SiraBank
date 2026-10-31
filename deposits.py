import json
import datetime 
username = input("Enter username, example: user01, user02, user03 :")
# data ile elaqelendirme
with open("data.json", "r", encoding="utf-8") as fayl:
    data = json.load(fayl)

if username not in data["accounts"]:
    print("User not found.")
else:
    account = data["accounts"][username]
    print("Balance:", account["balance"], "AZN")
    try:
        amount = float(input("Enter deposit amount: "))
    except ValueError:
        print("Error: enter a number only.")
        amount = 0

    if amount <= 0:
        print("Amount must be greater than 0.")
    else:
        today = str(datetime.date.today())
        # fayldaki tarixnen eyni deylse,demeli yeni gundu
        if account.get("deposit_date") != today:
            account["deposit_date"] = today
            account["deposited_today"] = 0

        remaining_limit = 2000 - account["deposited_today"]

        if amount > remaining_limit:
            print("Rejected. Remaining limit for today:", remaining_limit, "AZN")
        else:
            account["balance"] = account["balance"] + amount
            account["deposited_today"] = account["deposited_today"] + amount
            data["atmcash"] = data["atmcash"] + amount
            # dəyişiklikləri fayla yazırıq yoxsa proqram bağlananda itəcək
            with open("data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            print("Deposit successful. New balance:", account["balance"], "AZN")