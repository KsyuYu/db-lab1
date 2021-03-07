import csv
import os
import logging
import psycopg2

from datetime import datetime
from psycopg2.errors import lookup

LOG = logging.getLogger(__name__)
logging.basicConfig(filename="database_logs.log", level=logging.INFO, format="%(asctime)s: %(message)s")


def create_table(conn, cursor):
    LOG.info("Creating table")
    with open('queries/CreateGeneralTable.sql') as create_file:
        general_table_create = create_file.read()
    try:
        cursor.execute(general_table_create)
        LOG.info("GeneralTable has created")
    except lookup("42P07"):
        LOG.info("GeneralTable already exists")
    conn.commit()


def write_last_row(year, line):
    open('LastRow.txt', 'w').close()  # clean previous data from file
    with open('LastRow.txt', "w") as file:
        file.write(f"{year}, {line // 10 * 10}")


def read_last_row():
    with open('LastRow.txt', "r") as file:
        try:
            year, row = file.read().split(",")
        except ValueError:
            year, row = "2019", "0"
    return year, row


def insert_data(conn, cursor, csv_filename, year, start, last_row=0):
    LOG.info(f"Inserting data from {last_row} row from {csv_filename}")
    with open(csv_filename, encoding="cp1251") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        i = 0
        while i <= last_row:
            print(i)
            next(csv_reader, None)
            i += 1

        for row in csv_reader:
            print(i)
            insert_query = f"INSERT INTO GeneralTable VALUES({year}, "
            for value in row:
                try:
                    value = value.replace(",", ".")
                    float(value)
                except ValueError:
                    if value != "null":
                        value = "'" + value.replace("'", "`") + "'"
                insert_query += value + ", "

            insert_query = insert_query[:-2]  # delete last space and comma
            insert_query += ");"
            try:
                cursor.execute(insert_query)
                if i % 10 == 0:
                    conn.commit()
            except Exception as e:
                write_last_row(year, last_row + i)
                end_time = datetime.now()
                LOG.info(f"Broken at {end_time}")
                LOG.info(f"Work time {end_time - start}")
                raise e

            i += 1

    try:
        conn.commit()
    except Exception as e:
        raise e


def get_query(cursor):
    """Варіант №5. Порівняти середній бал з Історії України у кожному регіоні у 2020 та 2019 роках серед тих кому
    було зараховано тест"""
    LOG.info("Getting data for query")
    query = f"""Select regname, testyear, AVG(histball100)::Numeric(10, 3) AS histAverage
    From GeneralTable
    Where histteststatus = 'Зараховано'
    Group by regname, testyear
    Order by regname"""
    csv_query = f"COPY ({query}) TO STDOUT WITH CSV HEADER"

    with open("query.csv", 'w') as f:
        cursor.copy_expert(csv_query, f)
    LOG.info(f"Query data has recorded into query.csv")


def run():
    conn = psycopg2.connect(
        dbname=os.environ.get("name"),
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        host=os.environ.get("host")
    )
    cursor = conn.cursor()
    create_table(conn, cursor)

    year, row = read_last_row()
    row = int(row)
    start_time = datetime.now()
    if year == "2019":
        insert_data(conn, cursor, f"Odata2019File.csv", 2019, last_row=row, start=start_time)
        insert_data(conn, cursor, f"Odata2020File.csv", 2020, start=start_time)
    else:
        insert_data(conn, cursor, f"Odata2020File.csv", 2020, last_row=row, start=start_time)

    end_time = datetime.now()
    LOG.info(f"Finish inserting at {end_time}")
    LOG.info(f"Work time {end_time - start_time}")

    get_query(cursor)
    conn.commit()

    cursor.close()
    conn.close()

    LOG.info("The end")


if __name__ == "__main__":
    run()

#  number of all rows in files = 733112
