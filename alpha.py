import sqlite3

omega=sqlite3.connect('omega.db')
cursor=omega.cursor()

cursor.execute('''
       CREATE TABLE IF NOT EXISTS abilities(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL,
       basic_jutsu TEXT NOT NULL,
       clan TEXT NOT NULL,
       alein_otsutsuki TEXT NOT NULL,
       additional_abilities TEXT NOT NULL
          )
          
''')
omega.commit()
print("database created")
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS karma_users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
       hax INTEGER NOT NULL,
       speed INTEGER NOT NULL,
       iq INTEGER NOT NULL,
       battle_iq INTEGER NOT NULL,
       durability INTEGER NOT NULL,
       eye_factor TEXT NOT NULL,
       regeneration INTEGER NOT NULL,
       otsutsuki TEXT NOT NULL,
       tailed_beasts TEXT NOT NULL,
       junchuriki TEXT NOT NULL
       )
    """
)
omega.commit()
print("Karma_users table created")
