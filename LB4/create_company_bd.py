import sqlite3
import random
from datetime import datetime, timedelta


first_names = [
    "Алексей", "Мария", "Иван", "Елена", "Сергей", "Ольга", "Дмитрий", "Анна",
    "Андрей", "Наталья", "Павел", "Татьяна", "Михаил", "Юлия", "Артём", "Ксения",
    "Владимир", "Дарья", "Роман", "Екатерина", "Николай", "Светлана", "Виктор",
    "Ирина", "Станислав", "Валерия", "Григорий", "Полина", "Борис", "Алина"
]

last_names = [
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Соколов", "Лебедев", "Козлов",
    "Новиков", "Морозов", "Петров", "Волков", "Соловьёв", "Васильев", "Зайцев",
    "Павлов", "Семёнов", "Голубев", "Виноградов", "Богданов", "Воробьёв",
    "Фёдоров", "Михайлов", "Беляев", "Тарасов", "Белов", "Комаров", "Орлов",
    "Киселёв", "Макаров", "Андреев"
]

departments = ["IT", "HR", "Finance", "Logistics", "Marketing", "Sales", "Support", "Legal"]


conn = sqlite3.connect('company_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL,
    hire_date TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS logistic_bonus (
    id INTEGER PRIMARY KEY,
    bonus REAL NOT NULL,
    FOREIGN KEY (id) REFERENCES Employees(id)
)
''')


employees = []
start_date = datetime(2015, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = (end_date - start_date).days

for i in range(1, 121):
    first = random.choice(first_names)
    last = random.choice(last_names)
    full_name = f"{first} {last}"
    department = random.choice(departments)
    salary = round(random.uniform(40000, 150000), 2)
    random_days = random.randint(0, date_range)
    hire_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
    
    employees.append((i, full_name, department, salary, hire_date))


cursor.executemany('''
INSERT INTO Employees (id, full_name, department, salary, hire_date)
VALUES (?, ?, ?, ?, ?)
''', employees)

conn.commit()
conn.close()
