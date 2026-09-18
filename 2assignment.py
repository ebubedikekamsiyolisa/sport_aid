name=str(input("what is your name?:"))
password=int(input("Password needed:"))

if not name or not password :
    print("Invalid credentials")
else:
    print("log in successful")