import datetime

from storage import load_data


def show_limits(data, username):
    account = data["accounts"][username]
    today = str(datetime.date.today())

    # faylda saxlanan tarix bu gündürsə, saxlanan məbləği götürürük
    # başqa gündürsə (və ya heç nə yoxdursa), bu gün hələ pul yatırılmayıb
    if account.get("deposit_date") == today:
        deposited_today = account["deposited_today"]
    else:
        deposited_today = 0

    remaining_limit = 2000 - deposited_today

    # çıxarış: sayğac counter_date ilə sıfırlanır (atmtransfer.py ilə eyni qayda)
    if account.get("counter_date") == today:
        withdrawn_today = account.get("withdrawn_today", 0.0)
    else:
        withdrawn_today = 0.0

    # köçürmə: togrul.py gündəlik sayı dd.mm.yyyy açarı ilə saxlayır
    transfers_today = data.get("daily_transfers", {}).get(username, {}).get(
        datetime.date.today().strftime("%d.%m.%Y"), 0)

    print("Daily limits")
    print("Deposited today:", deposited_today, "/ 2000 AZN")
    print("Remaining deposit limit:", remaining_limit, "AZN")
    print(f"Withdrawn today: {withdrawn_today:.2f} / 1000.00 AZN")
    print(f"Remaining withdraw limit: {1000.0 - withdrawn_today:.2f} AZN")
    print("Transfers today:", transfers_today, "/ 5")


# fayli tek basina da islətmək olar: python limits.py
if __name__ == "__main__":
    data = load_data()
    username = input("Enter username (user01, user02, user03): ")
    if username not in data["accounts"]:
        print("User not found.")
    else:
        show_limits(data, username)