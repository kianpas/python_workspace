import sqlite3
import streamlit as st
import pandas as pd

conn = sqlite3.connect("test.db")

cur = conn.cursor()

st.title("sqlite 테스트")

create = st.button("테이블 생성")

insert = st.button("입력")

fetch = st.button("fetch")

delete = st.button("delete")

cur.execute("select count(*) from employee_data")

nums = cur.fetchone()
print(nums[0])
for num in nums:
    print(num)

if create and nums[0] <= 0:
    conn.execute(
        "CREATE TABLE employee_data(id INTEGER, name TEXT, nickname TEXT, department TEXT, employment_date TEXT)"
    )

    conn.commit()
    conn.close()

if insert:
    cur.executemany(
        "INSERT INTO employee_data VALUES (?, ?, ?, ?, ?)",
        [
            (1001, "Donghyun", "SOMJANG", "Development", "2020-04-01 00:00:00.000"),
            (2001, "Sol", "Fairy", "Marketing", "2020-04-01 00:00:00.000"),
            (2002, "Jiyoung", "Magician", "Marketing", "2020-04-01 00:00:00.000"),
            (1002, "Hyeona", "Theif", "Development", "2020-04-01 00:00:00.000"),
            (1003, "Soyoung", "Chief", "Development", "2020-04-01 00:00:00.000"),
        ],
    )
    conn.commit()
    conn.close()

if fetch:
    cur.execute("SELECT * FROM employee_data")

    rows = cur.fetchall()

    for row in rows:
        print(row)
    cols = [column[0] for column in cur.description]

    df = pd.DataFrame.from_records(data=rows, columns=cols)
    st.dataframe(df)
    conn.close()

if delete:
    cur.execute("delete from employee_data;")
    conn.commit()
    conn.close()
