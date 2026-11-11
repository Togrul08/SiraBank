import datetime
import math

from storage import load_data, save_data


def withdraw(data, username):
    account = data["accounts"][username]

    today = str(datetime.date.today())
    if account.get("counter_date") != today:
        account["counter_date"] = today
        account["withdrawn_today"] = 0.0

    print("Current Balance:", account["balance"], "AZN")
    try:
        amount = float(input("Enter withdrawal amount (AZN): "))
    except ValueError:
        print("Error: Please enter a valid number only.")
        amount = 0

    # nan / inf kimi qeyri-real ədədlər də qəbul olunmur
    if amount <= 0 or not math.isfinite(amount):
        print("Error: Amount must be greater than 0.")
    else:
        amount = round(amount, 2)
        DAILY_LIMIT = 1000.0
        withdrawn_today = account.get("withdrawn_today", 0.0)

        if withdrawn_today + amount > DAILY_LIMIT:
            remaining = DAILY_LIMIT - withdrawn_today
            print(f"Transaction rejected. Daily limit exceeded! You can withdraw up to {remaining:.2f} AZN more today.")

        elif amount > data.get("atmcash", 0.0):
            print("Transaction rejected. Insufficient cash in the ATM machine.")

        else:
            free_tier_left = max(0.0, 500.0 - withdrawn_today)
            excess_amount = max(0.0, amount - free_tier_left)
            commission = round(excess_amount * 0.02, 2)

            total_deduction = amount + commission
            balance_before = account["balance"]

            # balans yoxlanisi
            if balance_before < total_deduction:
                print(f"Transaction rejected. Insufficient balance for amount + commission (Required: {total_deduction:.2f} AZN).")
            else:
                account["balance"] = round(balance_before - total_deduction, 2)
                data["atmcash"] = round(data["atmcash"] - amount, 2)
                account["withdrawn_today"] = round(withdrawn_today + amount, 2)

                # Qebz
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                record = {
                    "time": now_str,
                    "type": "Withdraw",
                    "amount": round(amount, 2),
                    "commission": round(commission, 2),
                    "balance_after": account["balance"]
                }
                account["history"].append(record)

                # melumatlar jsonda saxlanilir
                save_data(data)

                print("\nWithdrawal successful!")
                print(f"Withdrawn amount : {amount:.2f} AZN")
                print(f"Commission fee   : {commission:.2f} AZN")
                print(f"Total deducted   : {total_deduction:.2f} AZN")
                print(f"New balance      : {account['balance']:.2f} AZN")
                print(f"Withdrawn today  : {account['withdrawn_today']:.2f} / 1000.00 AZN")


# fayli tek basina da islətmək olar: python atmtransfer.py
if __name__ == "__main__":
    data = load_data()
    username = input("Enter username (e.g. user01, user02): ")
    if username not in data["accounts"]:
        print("Error: User not found.")
    else:
        withdraw(data, username)