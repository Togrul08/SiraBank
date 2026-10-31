import json
with open("data.json", "r", encoding="utf-8") as file: #json faylini acib melumatlari oxuyuruq
    data = json.load(file)
current_user="user03"
current_balance = data["accounts"][current_user]["balance"] #istifadecinin cari balansi birbasa jsondan goturulur
atm_cash_reserve = data["atmcash"] #atm movcud nagd ehtiyati birbasa json goturulur
daily_withdrawn_total = 0.0 #bugunku cixarilan mebleg
amount = float(input("Çıxarmaq istədiyiniz məbləği daxil edin (AZN): "))
if daily_withdrawn_total+amount>1000:
    print("Xəta:Gündəlik çıxarma limiti aşılır!")
elif amount>atm_cash_reserve:
    print("Xəta:ATM-də kifayət qədər nağd pul yoxdur. Əməliyyat rədd edildi.")
elif amount<=0:
    print("Xəta:Etibarsız məbləğ daxil etdiniz.")
else:
    free_limit=500
    commission=0
    if daily_withdrawn_total>=free_limit:
        commission=amount*0.02
    elif daily_withdrawn_total+amount>free_limit:
        exceed_part=(daily_withdrawn_total+amount)-free_limit
        commission=exceed_part*0.02
    total_deduction=amount+commission
if current_balance<total_deduction:
        print("Xəta: Balansınız kifayət deyil.")
else:
     data["accounts"][current_user]["balance"] -= total_deduction
     data["atmcash"] -= amount
     with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
     print("\n--- ƏMƏLİYYAT UĞURLUDUR ---")
     print(f"Çıxarılan məbləğ: {amount} AZN")
     print(f"Tutulan komissiya: {commission} AZN")
     print(f"Yeni balansınız: {data['accounts'][current_user]['balance']} AZN")
     print(f"ATM-də qalan nağd pul: {data['atmcash']} AZN")

