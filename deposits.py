import datetime
import math

from storage import load_data, save_data


def deposit(data, username):
    account = data["accounts"][username]
    print("Balance:", account["balance"], "AZN")
    try:
        amount = float(input("Enter deposit amount: "))
    except ValueError:
        print("Error: enter a number only.")
        amount = 0

    # nan / inf kimi qeyri-real ədədlər də qəbul olunmur
    if amount <= 0 or not math.isfinite(amount):
        print("Amount must be greater than 0.")
    else:
        amount = round(amount, 2)
        today = str(datetime.date.today())
        # fayldaki tarixle eyni deyilse, demeli yeni gundur
        if account.get("deposit_date") != today:
            account["deposit_date"] = today
            account["deposited_today"] = 0

        remaining_limit = round(2000 - account["deposited_today"], 2)

        if amount > remaining_limit:
            print("Rejected. Remaining limit for today:", remaining_limit, "AZN")
        else:
            balance_before = account["balance"]

            account["balance"] = round(account["balance"] + amount, 2)
            account["deposited_today"] = round(account["deposited_today"] + amount, 2)
            data["atmcash"] = round(data["atmcash"] + amount, 2)
            # tarixce ucun qeyd
            record = {
                "transaction_id": len(data["history"]) + 1,
                "username": username,
                "type": "deposit",
                "amount": amount,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "balance_before": balance_before,
                "balance_after": account["balance"],
                "other_account": None,
                "commission": 0
            }
            # siyahiya elave edirik
            data["history"].append(record)

            # deyisiklikleri fayla atirig
            save_data(data)

            print("Deposit successful. New balance:", account["balance"], "AZN")


# fayli tek basina da islətmək olar: python deposits.py
if __name__ == "__main__":
    data = load_data()
    username = input("Enter username, example: user01, user02, user03 :")
    if username not in data["accounts"]:
        print("User not found.")
    else:
        deposit(data, username)