import sqlite3

epsilon=sqlite3.connect('health.db')
cursor=epsilon.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS patients (
       id_of_patients INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       name TEXT NOT NULL,
       gender TEXT NOT NULL,
       age INTEGER NOT NULL,
       house_address TEXT NOT NULL,
       ailments TEXT NOT NULL,
       current_statues TEXT NOT NULL
          )
          
""")
epsilon.commit()


cursor.execute("""INSERT INTO patients(name, gender, age, house_address, ailments, current_statues)
       VALUES('Allen_snow','Male',20,'Mercury','Frozen_allergy','healed'),
       ('Peters_hot','Male',21,'Venus','Cold_bites','healed'),
       ('Andy_green','Male',18,'Earth','Healthy','healed'),
       ('Marty_swift','Female',22,'Mars','Barren','healed'),
       ('Huge_might','Male',30,'Jupiter','Obesity','healed'),
       ('Angela_ring','Female',27,'Saturn','Ringworm','healed'),
       ('Nickel_brown','Female',28,'Uranus','Hydrophobia','healed'),
       ('Diamond_white','Male',25,'Neptune','Thermophobia','healed'),
       ('Oliver_littleton','Male',7,'Pluto','Dwarfism','healed'),
       ('Alchemy_luff','Male',9,'Hermes','Bald','healed'),
       ('Barbey_michel','Female',5,'Kepler','Premature','healed'),
       ('Baby_lunar','Female',9,'Moon','Timidity','healed')
       """)
epsilon.commit()
epsilon.close()

print("database created")