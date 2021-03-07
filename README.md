# Лабораторна робота №1 студентки групи КМ-81 Юр'єваї Ксенії

Перед запуском програми додайте в папку проекту файли *Odata2019File.csv*, *Odata2020File.csv*

## Інструкція по запуску

В окремому терміналі/консолі запустити

- `docker-compose up`

В браузері відкрити PGAdmin: http://localhost:8081

- Логін та пароль до PGAdmin: `admin@kpi.ua`, `admin`

В лівому вікні натиснути правою кнопкою миші на _Servers_ і обрати _Create -> Server_

- Логін та пароль до сервера: `postgres`
- Host name: `db`

Послідовно виконати наступні команди:

- Linux/MacOS

```bash
python3 -m pip install virtualenv
python3 -m venv env
source env/bin/activate
source .env
python3 -m pip install -r requirements.txt
python3 main.py
```

- Windows

```
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
env.bat
py -m pip install -r requirements.txt
py main.py
```

## Результати роботи програми

### Таблиця

#### Перші три рядки та стовпці з таблиці GeneralTable

testyear|outid|birth
--- |--- |---
2019 | 07ad4c55-70ef-442d-bb7f-34c95c0e6ee4 | 2001
2019 | 8626c448-3a7d-434f-b01a-c2530ccf3a4f | 1985
2019 | 9709b00b-144c-4487-b7bc-66c0b353b324 | 2001

#### Приклад файлу LastRow.txt

2019, 11370

#### Приклад файлу database_logs.log

Протягом роботи програма записує свої дії у файл database_logs.log.  
На початку і в кінці додавання даних фіксується час поточної ітерації. Наприклад, `Work time 0:00:38.678979`

Приклад логів при одному падінні бази

```
2021-03-07 18:01:14,334: Creating table
2021-03-07 18:01:14,402: GeneralTable has created
2021-03-07 18:01:14,410: Inserting data from 1 row from Odata2019File.csv
2021-03-07 18:01:53,089: Broken at 2021-03-07 18:01:53.089839
2021-03-07 18:01:53,089: Work time 0:00:38.678979
2021-03-07 18:02:45,063: Creating table
2021-03-07 18:02:45,069: GeneralTable already exists
2021-03-07 18:02:45,074: Inserting data from 11370 row from Odata2019File.csv
2021-03-07 18:21:25,201: Inserting data from 1 row from Odata2020File.csv
2021-03-07 18:42:15,774: Finish inserting at 2021-03-07 18:42:15.773086
2021-03-07 18:42:15,775: Work time 0:39:30.698775
2021-03-07 18:42:15,775: Getting data for query
2021-03-07 18:42:16,675: Query data has recorded into query.csv
2021-03-07 18:42:16,677: The end
```

#### Файл query.csv

Отриманий файл є результатом роботи програми. Згідно із завданням `Варіант 5. Порівняти середній бал з Історії України у кожному регіоні у 2020 та 2019 роках серед тих кому було зараховано тест` у файлі наведені відомості про регіон, рік проведення ЗНО та середній бал з історії.