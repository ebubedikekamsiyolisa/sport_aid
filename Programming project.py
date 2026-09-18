import sqlite3

gamma=sqlite3.connect("NIIT.db")
cursor=gamma.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS students(
               id_of_students INTEGER PRIMARY KEY AUTOINCREMENT,
               surname TEXT NOT NULL,
               firstname TEXT NOT NULL,
               home_address TEXT NOT NULL,
               gender TEXT NOT NULL,
               age INTEGER NOT NULL,
               program_study TEXT NOT NULL,
               amount_of_payment INTEGER NOT NULL
                  )
                  
""")

gamma.commit()


cursor.execute( """INSERT INTO students(surname,firstname,home_address,gender,age,program_study,amount_of_payment)
               VALUES('Ndigwe','Ifechukwu','Wakanda','Male',16,'Python', 1500),
               ('Obijiofor','Kenechukwu','Hiddensand','Male',17,'Python', 1500),
               ('Ifeanyi','Ekene','Darkhold','Male',18,'Python', 1500),
               ('Chibuike','Chidera','snowland','Male',17,'Python', 1500),
               ('Ewenike','Chibueze','Hiddenleaf','Male',16,'Forex', 1500),
               ('Aliwaonu','Ogechukwu','Stronghold','Male',18,'Java', 1500),
               ('Ikediashi','Jessi','Plutomania','Male',17,'Web_design', 1500)   
                """)

gamma.commit()
gamma.close()


print("database created")