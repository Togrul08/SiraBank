import json
import os

data_file = "data.json"

def load_data():
    if not os.path.exists(data_file):
        return {
            "accounts": {
                "user01":{"Password":"Test123" , "balance":2500.00},
                "user02":{"Password":"Test456" , "balance":1500.00},
                "user03":{"Password":"Test789" , "balance":3000.00}
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


if __name__ == "__main__":
    data = load_data()
    save_data(data)
    print("JSON melumatlarndi yuklendi musteri")