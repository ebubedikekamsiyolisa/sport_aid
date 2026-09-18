import sqlite3

gamma=sqlite3.connect("NIIT.db")
cursor=gamma.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS students (
               id_of_student INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
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


cursor.execute("""INSERT INTO students(surname,firstname,home_address,gender,age,program_study,amount_of_payment)
              VALUES('Ndigwe','Ifechukwu','Wakanda','Male',16,'Python',$1500),
              ('Obijiofor','Kenechukwu','Hidden_sand','Male',17,'Python',$1500),
              ('Ewenike','Chibueze','Hidden_leaf','Male',16,'Forex',$2000),
              ('Ifeanyi','Ekene','Dark_hold','Male',18,'Python',$1500),
              ('Chibuike','Chidera','Land_of_bones','Male',17,'Web_design',$1000),
              ('Nwadigwu','Chinedu','Land_of_masquerade','Male',18,'Web_design',$1000),
              ('Aliwaonu','Ogechukwu','Castle_of_titans','Male',18,'Java',$3000),
              ('Ikediashi','Jessi','Hidden_mist','Male',16,'Forex',$2000)
               """)
gamma.commit()
gamma.close()


print("database created")