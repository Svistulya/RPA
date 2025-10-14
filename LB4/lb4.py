# Вариант № 5
import sqlite3

conn = sqlite3.connect('company_data.db')
cursor = conn.cursor()

cursor.execute("SELECT id, salary FROM Employees WHERE department = 'Logistics'")
logistics_employees = cursor.fetchall()

bonus_records = []
for emp_id, salary in logistics_employees:
    bonus = round(salary * 0.15, 2)  
    bonus_records.append((emp_id, bonus))

cursor.executemany('''
INSERT INTO logistic_bonus (id, bonus)
VALUES (?, ?)
''', bonus_records)

conn.commit()
conn.close()
