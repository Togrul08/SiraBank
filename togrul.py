import math
from datetime import datetime
from storage import load_data, save_data


def transfer(data, sender=None):
    # giris.py-dan çağırılanda göndərən artıq məlumdur (daxil olmuş istifadəçi);
    # fayl tək başına işlədilərsə, əvvəlki kimi soruşulur
    if sender is None:
        sender = input("Pul gönderen: ")
    receiver = input("Qebul eden istifadeçi: ")


    if sender not in data["accounts"]:
        print("Gönderen istifadeçi tapılmadı")
        return
    today = datetime.now().strftime("%d.%m.%Y")
    daily_transfers = data.setdefault("daily_transfers", {})
    user_transfers = daily_transfers.get(sender, {})
    if user_transfers.get(today, 0) >= 5:
        print("Gündəlik köçürmə limitiniz bitib. Maksimum 5 köçürmə edə bilərsiniz.")
        return

    if receiver not in data["accounts"]:
        print("Qebul eden istifadeçi tapılmadı")
        return

    if sender == receiver:
        print("Öz hesabıva pul ata bilmersen")
        return


    try:
        amount = float(input("Köçürülecek mebleği seç: "))
    except ValueError:
        print("Zehmet olmasa mebleği düzgün seçin")
        return



    if amount <= 0 or not math.isfinite(amount):
        print("Pul menfi ve sıfır ola bilmez")
        return

    amount = round(amount, 2)


    if amount > data["accounts"][sender]["balance"]:
        print("Hörmetli abunetçi balansınızda kifayet qeder vesait yoxdur lütfen balansınızı atrırınız!!!")
        return


    while True:
        confirm = input("Köçürmeni tesdiq edirsiniz?: (Yes/No)").lower().strip()

        if confirm == "yes":
            break
        elif confirm == "no":
            print("Köçürme leğv edildi")
            return
        else:
            print("Yanlış seçim")


    data["accounts"][sender]["balance"] = round(data["accounts"][sender]["balance"] - amount, 2)
    data["accounts"][receiver]["balance"] = round(data["accounts"][receiver]["balance"] + amount, 2)
    
    data["history"].append({
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    })

    data["daily_transfers"].setdefault(sender, {})
    data["daily_transfers"][sender][today] = data["daily_transfers"][sender].get(today, 0) + 1

    save_data(data)


    print("Köçürme uğurla tamamlandı")
    print(f"Gönderenin yeni balansı: {data['accounts'][sender]['balance']}")
    print(f"Qebul edenin yeni balansı: {data['accounts'][receiver]['balance']}")


def parse_time(text):
    """Fərqli fayllar tarixi fərqli formatda yazır; hamısını oxuya bilirik."""
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(text), fmt)
        except ValueError:
            pass
    return datetime.min


def view_history(data, current_user):
    """
    Əməliyyatlar fərqli yerlərdə saxlanılır, burda hamısı birlikdə göstərilir:
      - deposits.py      -> data["history"]  (username / type / amount / date)
      - togrul.py        -> data["history"]  (sender / receiver / amount / date)
      - atmtransfer.py   -> hesabın öz history siyahısı (time / type / amount / commission)
    """
    entries = []   # (vaxt_obyekti, vaxt_yazısı, ad, işarə, məbləğ, komissiya, balans_sonra)

    for transaction in data.get("history", []):
        if transaction.get("username") == current_user:
            kind = str(transaction.get("type", "?")).capitalize()
            sign = "-" if kind.lower() == "withdraw" else "+"
            entries.append((parse_time(transaction.get("date")), str(transaction.get("date")), kind, sign,
                            transaction.get("amount", 0), transaction.get("commission", 0),
                            transaction.get("balance_after")))
        elif transaction.get("sender") == current_user or transaction.get("receiver") == current_user:
            if transaction.get("sender") == current_user:
                kind = "Transfer Out to " + str(transaction.get("receiver"))
                sign = "-"
            else:
                kind = "Transfer In from " + str(transaction.get("sender"))
                sign = "+"
            entries.append((parse_time(transaction.get("date")), str(transaction.get("date")), kind, sign,
                            transaction.get("amount", 0), 0, None))

    account = data["accounts"].get(current_user, {})
    for transaction in account.get("history", []):
        kind = str(transaction.get("type", "?")).capitalize()
        sign = "-" if kind.lower() == "withdraw" else "+"
        entries.append((parse_time(transaction.get("time")), str(transaction.get("time"))[:19], kind, sign,
                        transaction.get("amount", 0), transaction.get("commission", 0),
                        transaction.get("balance_after")))

    if not entries:
        print("Emeliyyat tarixcesi boşdur")
        return

    entries.sort(key=lambda item: item[0])
    print("Transaction History")
    print("-" * 78)
    for _, when, kind, sign, amount, commission, balance_after in entries:
        line = f"{when} | {kind.ljust(22)} | {sign}{float(amount):.2f} AZN"
        if commission:
            line += f" (fee {float(commission):.2f})"
        if balance_after is not None:
            line += f" | Balance: {float(balance_after):.2f} AZN"
        print(line)


  


if __name__ == "__main__":
    data = load_data()
    while True:
        transfer(data)
        history_choice = input("Emeliyyat tarixcesine baxmaq isteyirsiniz? (Yes/No): ").lower().strip()
        if history_choice == "yes":
            current_user = input("Username daxil edin:")
            view_history(data, current_user)
        
        choice = input("\nYenidən köçürmə etmək istəyirsiniz? (Yes/No): ").lower().strip()

        if choice == "no":
            print("Proqramdan çıxılır.")
            break

        elif choice != "yes":
            print("Yanlış seçim!")
            break