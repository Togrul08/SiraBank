import json
import math
import os
import time
from datetime import datetime
 
FILE_NAME = "bank_data.json"
DAILY_DEPOSIT_LIMIT = 2000.00
LOCK_SECONDS = 60
MAX_ATTEMPTS = 6
 
today = datetime.now().strftime("%Y-%m-%d")
 
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        data = json.load(f)
else:
    data = {"atm_cash": 10000.00, "users": {}}
 
    default_users = [
        ("user01", "Test@123", 2500.00, "10010001"),
        ("user02", "Test@456", 1500.00, "10010002"),
        ("user03", "Test@789", 3000.00, "10010003"),
    ]
 
    for item in default_users:
        data["users"][item[0]] = {
            "password": item[1],
            "account_number": item[3],
            "balance": item[2],
            "blocked": False,
            "failed_attempts": 0,
            "lockout_until": 0,
            "counter_date": today,
            "deposited_today": 0.0,
            "withdrawn_today": 0.0,
            "transfer_count": 0,
            "history": [],
            "last_login": "Never",
            "last_transaction": "Never",
        }
 
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)
    print("First run: demo accounts created.")