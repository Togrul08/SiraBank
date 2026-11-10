# SiraBank – Bank Management System

## 1. Layihənin məqsədi

SiraBank Python proqramlaşdırma dili ilə hazırlanmış sadə bank idarəetmə sistemidir. Layihənin məqsədi bank əməliyyatlarını rəqəmsal formada həyata keçirmək və istifadəçilərin hesablarını idarə etməkdir.

Sistem aşağıdakı funksiyaları əhatə edir:
- İstifadəçi autentifikasiyası (Login)
- Hesab balansının yoxlanılması
- Pul yatırılması (Deposit)
- Pul çıxarılması (Withdraw)
- Hesablararası pul köçürülməsi (Transfer)
- ATM balansının idarə edilməsi
- Əməliyyat tarixçəsinin göstərilməsi
- Gündəlik əməliyyat limitlərinin tətbiqi

## 2. İstifadə olunan texnologiyalar

- Python 3.8+
- JSON – məlumatların saxlanılması
- Git və GitHub – versiya nəzarəti
- VS Code – kod redaktoru

Layihədə Python-un standart kitabxanalarından istifadə olunur.

## 3. Proqramın işə salınması

1. Layihəni kompüterə yükləyin.
2. Layihə qovluğunu VS Code-da açın.
3. Terminalı başladın.
4. Əsas proqram faylını işə salın.

```bash
python main.py
```

Qeyd: Əsas giriş faylının adı layihənin yekun strukturuna uyğun olmalıdır.

## 4. Demo hesablar

| Username | Password | Balance |
|---|---|---:|
| user01 | Test@123 | 2500 AZN |
| user02 | Test@456 | 1500 AZN |
| user03 | Test@789 | 3000 AZN |

İlkin ATM balansı: **5000 AZN**

## 5. Əməliyyat limitləri

- Bir istifadəçi gündə maksimum 5 pul köçürməsi edə bilər.
- Mənfi və sıfır məbləğlə əməliyyat aparıla bilməz.
- Balansda kifayət qədər vəsait olmadıqda əməliyyat həyata keçirilmir.
- İstifadəçi öz hesabına pul köçürə bilməz.
- Bütün əməliyyatlar tarixçədə saxlanılır.

## 6. Layihənin qovluq strukturu

```text
SiraBank/
│
├── data.json
├── storage.py
├── main.py
├── togrul.py
├── authentication.py
├── deposits.py
├── withdrawals.py
├── README.md
└── .gitignore
```

Qeyd: Fayl adları yekun komanda strukturuna uyğunlaşdırılmalıdır.

## 7. Komanda üzvləri və vəzifələri

1. Togrul Aslanov – Pul köçürmələri (Transfers), əməliyyat tarixçəsi və məlumatların saxlanılması.
2. Suad Alixanlı – İstifadəçi autentifikasiyası (Authentication).
3. Vusal Hadiyev – Pul yatırılması və limitlər (Deposits & Limits).
4. Aysu Cafarli – Pul çıxarılması və ATM sistemi (Withdrawals & ATM).

## 8. Testlər

Layihədə aşağıdakı ssenarilər yoxlanılmalıdır:

- Düzgün və yanlış login məlumatları.
- Balansın düzgün yenilənməsi.
- Kifayət qədər vəsait olmadıqda əməliyyatın dayandırılması.
- Yanlış məbləğ daxil edilməsi.
- Gündəlik köçürmə limitinin yoxlanılması.
- Əməliyyat tarixçəsinin düzgün göstərilməsi.
- JSON faylında məlumatların saxlanılması.

## 9. Məlum məhdudiyyətlər

- Layihə tədris məqsədilə hazırlanmış prototipdir.
- Məlumatlar JSON faylında saxlanılır.
- Şifrələr demo versiyada açıq mətn formasındadır.
- Real bank sistemləri üçün tələb olunan təhlükəsizlik mexanizmləri tam tətbiq edilməyib.
- Sistem real bank infrastrukturu ilə əlaqəli deyil.

## 10. Nəticə

SiraBank layihəsi Python vasitəsilə bank əməliyyatlarının avtomatlaşdırılmasını nümayiş etdirir. Layihə komanda şəklində hazırlanmış və modullu proqramlaşdırma, JSON ilə işləmə, funksiyaların yaradılması və GitHub üzərindən əməkdaşlıq bacarıqlarının inkişafına xidmət edir.