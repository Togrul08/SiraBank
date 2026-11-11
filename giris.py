import math
import os
import time
from datetime import datetime

from atmtransfer import withdraw
from deposits import deposit
from limits import show_limits
from storage import load_data, save_data
from togrul import transfer, view_history

# data.json həmişə bu faylın yanındakı qovluqda tapılsın
os.chdir(os.path.dirname(os.path.abspath(__file__)))

FILE_NAME = "data.json"
LOCK_SECONDS = 60
MAX_ATTEMPTS = 6

today = datetime.now().strftime("%Y-%m-%d")

if os.path.exists(FILE_NAME):
    data = load_data()
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

    save_data(data)
    print("First run: demo accounts created.")

# köhnə / natamam data.json üçün çatışmayan sahələri tamamlayırıq
data.setdefault("atmcash", 5000.00)
data.setdefault("history", [])
data.setdefault("daily_transfers", {})
for index, (name, account) in enumerate(data["accounts"].items(), start=1):
    account.setdefault("account_number", f"1001{index:04d}")
    account.setdefault("blocked", False)
    account.setdefault("failed_attempts", 0)
    account.setdefault("lockout_until", 0)
    account.setdefault("counter_date", "Never")
    account.setdefault("deposited_today", 0.0)
    account.setdefault("withdrawn_today", 0.0)
    account.setdefault("history", [])
    account.setdefault("last_login", "Never")
    account.setdefault("last_transaction", "Never")

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
            save_data(data)
            logged_in = True
            break
        else:
            user["failed_attempts"] += 1
            print("Incorrect password. Attempt: " + str(user["failed_attempts"]) + "/" + str(MAX_ATTEMPTS))

            if user["failed_attempts"] >= MAX_ATTEMPTS:
                user["blocked"] = True
            elif user["failed_attempts"] == 3:
                user["lockout_until"] = time.time() + LOCK_SECONDS

            save_data(data)

    if not logged_in:
        continue

    while True:
        # Qeyd: gündəlik sayğacların sıfırlanması indi deposits.py (deposit_date)
        # və atmtransfer.py (counter_date) daxilində edilir. Burda ayrıca sıfırlama
        # olsaydı, gün ərzində depozit limiti səhvən sıfırlanardı.

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
            print()
            deposit(data, username)            # deposits.py

        elif choice == "4":
            print()
            withdraw(data, username)           # atmtransfer.py

        elif choice == "5":
            print()
            transfer(data, username)           # togrul.py

        elif choice == "6":
            print()
            view_history(data, username)       # togrul.py

        elif choice == "7":
            print()
            show_limits(data, username)        # limits.py

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
                    save_data(data)
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