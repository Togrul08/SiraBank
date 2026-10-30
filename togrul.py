import json
import os

data_file = "data.json"

def load_data():
    if not os.path.exists(data_file):
        return {
            "accounts": {
                "user01":{"password":"Test@123" , "balance":2500.00},
                "user02":{"password":"Test@456" , "balance":1500.00},
                "user03":{"password":"Test@789" , "balance":3000.00}
            },
            "atmcash": 5000.00,
            "history": {},
            "daily_transfers": {}
        }

    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



def transfer(data):
    sender = input("Pul gönderen: ")
    receiver = input("Qebul eden istifadeçi: ")


    if sender not in data["accounts"]:
        print("Gönderen istifadeçi tapılmadı")
        return


    if receiver not in data["accounts"]:
        print("Qebul eden istifadeçi tapılmadı")
        return

    if sender == receiver:
        print("Öz hesabıva pul ata bilmersen")
        return


    amount = float(input("Köçürülecek mebleği seç: "))


    if amount <= 0:
        print("Pul menfi ve sıfır ola bilmez")
        return


    if amount > data["accounts"][sender]["balance"]:
        print("Hörmetli abunetçi balansınızda kifayet qeder vesait yoxdur lütfen balansınızı atrırın")
        return


    data["accounts"][sender]["balance"] = data["accounts"][sender]["balance"] - amount
    data["accounts"][receiver]["balance"] = data["accounts"][receiver]["balance"] + amount

    save_data(data)


    print("Köçürme uğurla tamamlandı")
    print(f"Gönderenin yeni balansı: {data['accounts'][sender]['balance']}")
    print(f"Qebul edenin yeni balansı: {data['accounts'][receiver]['balance']}")
    



if __name__ == "__main__":
    data = load_data()
    transfer(data)