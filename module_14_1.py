import sqlite3
import pprint

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER not null
)
''')


for i in range(10):
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)", (f"User{i+1}", f"example{i+1}@gmail.com", (i+1)*10, 1000))



for i in range(10):
    if not((i+1) % 2):
        name = str(f'User{i}')
        cursor.execute("UPDATE Users SET balance = ? WHERE username = ?", (500, name ))

    if not(i%3):
        name = str(f'User{i+1}')
        cursor.execute("DELETE FROM Users WHERE username = ?", (name,))



cursor.execute("SELECT username, email, age, balance  FROM Users WHERE age !=60")
users = cursor.fetchall()
for user in users:
    print(f'Имя:{user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')


connection.commit()
connection.close()

# Тут на каждом этапе можно упасть. Лучше, конечно как-то так:
# https://pythonru.com/biblioteki/obnovlenie-dannyh-v-sqlite-tablice

