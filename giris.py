import json
import math
import os
import time
from datetime import datetime

FILE_NAME = "data.json"
DAILY_DEPOSIT_LIMIT = 2000.00
LOCK_SECONDS = 60
MAX_ATTEMPTS = 6

today = datetime.now().strftime("%Y-%m-%d")

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        data = json.load(f)
else:
    data = {"atmcash": 5000.00, "accounts": {}, "history": [], "daily_transfers": {}}

    default_users = [
        ("user01", "Test@123", 2500.00, "10010001"),
        ("user02", "Test@456", 1500.00, "10010002"),
        ("user03", "Test@789", 3000.00, "10010003"),
    ]

    for item in default_users:
        data["accounts"][item[0]] = {
            "password": item[1],
            "account_number": item[3],
            "balance": item[2],
            "blocked": False,
            "failed_attempts": 0,
            "lockout_until": 0,
            "counter_date": today,
            "deposited_today": 0.0,
            "withdrawn_today": 0.0,
            "history": [],
            "last_login": "Never",
            "last_transaction": "Never",
        }
        data["daily_transfers"][item[0]] = {datetime.now().strftime("%d.%m.%Y"): 0}

    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)
    print("First run: demo accounts created.")

program_running = True

while program_running:
    print()
    print("=" * 36)
    print("        BANK LOGIN")
    print("=" * 36)
    username = input("Username (type 'exit' to quit): ").strip()

    if username.lower() == "exit":
        break

    if username not in data["accounts"]:
        input("Password: ")
        print("Invalid username or password.")
        continue

    user = data["accounts"][username]
    logged_in = False

    while True:
        if user["blocked"]:
            print("Maximum login attempts exceeded.")
            print("Your card has been blocked.")
            print("Please contact the bank administrator.")
            break

        if time.time() < user["lockout_until"]:
            print("Too many failed login attempts.")
            while time.time() < user["lockout_until"]:
                left = math.ceil(user["lockout_until"] - time.time())
                minutes = left // 60
                seconds = left % 60
                print("Please wait: " + str(minutes).zfill(2) + ":" + str(seconds).zfill(2))
                time.sleep(1)
            print("You may try again.")

        password = input("Password: ")

        if password == user["password"]:
            user["failed_attempts"] = 0
            user["lockout_until"] = 0
            user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(FILE_NAME, "w") as f:
                json.dump(data, f, indent=4)
            logged_in = True
            break
        else:
            user["failed_attempts"] += 1
            print("Incorrect password. Attempt: " + str(user["failed_attempts"]) + "/" + str(MAX_ATTEMPTS))

            if user["failed_attempts"] >= MAX_ATTEMPTS:
                user["blocked"] = True
            elif user["failed_attempts"] == 3:
                user["lockout_until"] = time.time() + LOCK_SECONDS

            with open(FILE_NAME, "w") as f:
                json.dump(data, f, indent=4)

    if not logged_in:
        continue

    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        if user["counter_date"] != today:
            user["counter_date"] = today
            user["deposited_today"] = 0.0
            user["withdrawn_today"] = 0.0
            with open(FILE_NAME, "w") as f:
                json.dump(data, f, indent=4)

        print()
        print("=" * 36)
        print("        PYTHON BANKING SYSTEM")
        print("=" * 36)
        print("Welcome, " + username + "!")
        print()
        print("1. View Account Information")
        print("2. Check Balance")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Transaction History")
        print("7. Daily Limits")
        print("8. Change Password")
        print("9. Logout")
        print("0. Exit")
        print("=" * 36)
        choice = input("Select an option: ").strip()

        if choice == "1":
            if user["blocked"]:
                status = "Blocked"
            else:
                status = "Active"
            print()
            print("Account Holder : " + username)
            print("Account Number : " + user["account_number"])
            print(f"Available Balance: {user['balance']:.2f} AZN")
            print("Account Status: " + status)

        elif choice == "2":
            print()
            print(f"Available Balance: {user['balance']:.2f} AZN")

        elif choice == "3":
            remaining = round(DAILY_DEPOSIT_LIMIT - user["deposited_today"], 2)
            print()
            print(f"Remaining deposit allowance: {remaining:.2f} AZN")
            text = input("Enter deposit amount: ").strip()

            valid = True
            if not text.replace(".", "", 1).isdecimal():
                valid = False
            elif "." in text and len(text.split(".")[1]) > 2:
                valid = False
            elif float(text) <= 0:
                valid = False

            if not valid:
                print("Invalid amount. Enter a positive number with at most 2 decimal places.")
            else:
                amount = round(float(text), 2)

                if amount > remaining:
                    print()
                    print(f"Deposited today: {user['deposited_today']:.2f} AZN")
                    print(f"Requested deposit: {amount:.2f} AZN")
                    print(f"Daily deposit maximum: {DAILY_DEPOSIT_LIMIT:.2f} AZN")
                    print(f"Remaining deposit allowance: {remaining:.2f} AZN")
                    print()
                    print("Deposit declined: daily limit would be exceeded.")
                    print("Account balance and ATM cash remain unchanged.")
                else:
                    now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    user["balance"] = round(user["balance"] + amount, 2)
                    data["atmcash"] = round(data["atmcash"] + amount, 2)
                    user["deposited_today"] = round(user["deposited_today"] + amount, 2)
                    user["last_transaction"] = now_text
                    user["history"].append({
                        "time": now_text,
                        "type": "Deposit",
                        "amount": amount,
                        "balance_after": user["balance"],
                    })
                    with open(FILE_NAME, "w") as f:
                        json.dump(data, f, indent=4)

                    remaining = round(DAILY_DEPOSIT_LIMIT - user["deposited_today"], 2)
                    print()
                    print(f"Deposit successful: {amount:.2f} AZN")
                    print(f"New balance: {user['balance']:.2f} AZN")
                    print(f"Remaining deposit allowance: {remaining:.2f} AZN")

        elif choice == "4":
            print()
            print("Withdraw is not implemented yet.")

        elif choice == "5":
            print()
            print("Transfer is not implemented yet.")

        elif choice == "6":
            print()
            if len(user["history"]) == 0:
                print("No transactions yet.")
            else:
                print("Transaction History")
                print("-" * 60)
                for record in user["history"]:
                    print(record["time"] + " | " + record["type"].ljust(10)
                          + f" | {record['amount']:.2f} AZN | Balance: {record['balance_after']:.2f} AZN")

        elif choice == "7":
            remaining = round(DAILY_DEPOSIT_LIMIT - user["deposited_today"], 2)
            print()
            print(f"Deposited today: {user['deposited_today']:.2f} AZN")
            print(f"Daily deposit maximum: {DAILY_DEPOSIT_LIMIT:.2f} AZN")
            print(f"Remaining deposit allowance: {remaining:.2f} AZN")

        elif choice == "8":
            print()
            old_password = input("Current password: ")
            if old_password != user["password"]:
                print("Current password is incorrect.")
            else:
                new1 = input("New password: ")
                new2 = input("Repeat new password: ")
                if len(new1) < 6:
                    print("Password must be at least 6 characters.")
                elif new1 == old_password:
                    print("New password must be different from the old one.")
                elif new1 != new2:
                    print("Passwords do not match.")
                else:
                    user["password"] = new1
                    with open(FILE_NAME, "w") as f:
                        json.dump(data, f, indent=4)
                    print("Password changed successfully.")

        elif choice == "9":
            print("You have been logged out.")
            break

        elif choice == "0":
            print("Goodbye!")
            program_running = False
            break

        else:
            print("Invalid option. Please choose a number from the menu.")