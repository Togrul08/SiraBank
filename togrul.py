from datetime import datetime
from storage import load_data, save_data


def transfer(data):
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



    if amount <= 0:
        print("Pul menfi ve sıfır ola bilmez")
        return


    if amount > data["accounts"][sender]["balance"]:
        print("Hörmetli abunetçi balansınızda kifayet qeder vesait yoxdur lütfen balansınızı atrırın")
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


    data["accounts"][sender]["balance"] = data["accounts"][sender]["balance"] - amount
    data["accounts"][receiver]["balance"] = data["accounts"][receiver]["balance"] + amount
    
    data["history"].append({
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M")
    })

    data["daily_transfers"].setdefault(sender, {})
    data["daily_transfers"][sender][today] = data["daily_transfers"][sender].get(today, 0) + 1

    save_data(data)


    print("Köçürme uğurla tamamlandı")
    print(f"Gönderenin yeni balansı: {data['accounts'][sender]['balance']}")
    print(f"Qebul edenin yeni balansı: {data['accounts'][receiver]['balance']}")


  


def view_history(data, current_user):
    found = False 
    for transaction in data["history"]:
        if transaction.get("sender") == current_user or transaction.get("receiver") == current_user or transaction.get("username") == current_user:
            print("Göndərən:", transaction["sender"])
            print("Qəbul edən:", transaction["receiver"])
            print("Məbləğ:", transaction["amount"])
            print("Tarix:", transaction["date"])

            found = True 

    if not found:
        print("Emeliyyat tarixcesi boşdur")


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