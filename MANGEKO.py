import sqlite3

alpha = sqlite3.connect('school.db')
cursor = alpha.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS student (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          age INTEGER NOT NULL,
          course TEXT NOT NULL,
          gender TEXT NOT NULL,
          score INTEGER NOT NULL
             ) 
""")

alpha.commit()


cursor.execute("""INSERT INTO student (name, age, course, gender, score)
    VALUES('hashirama', 27,'ninjitzu','male',97),
    ('tobirama', 24,'ninjitzu','male',91),
    ('hagoromo', 91,'ninjitzu','male',87),
    ('minato', 33,'ninjitzu','male',90),
    ('tsunade', 45,'ninjitzu','female',80),
    ('kakashi', 23,'ninjitzu','male',79)
    """)

alpha.commit()
alpha.close()


print("database created")