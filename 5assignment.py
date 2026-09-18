Participant=str(input("please enter your name:"))

if Participant =="kamsi":
    print("kamsi is back!")
if not Participant=="kamsi":
    print("access denied!")

Numbers= []
for i in range(5):
    while True:
        try:
            val=float(input(f"enter number{i+1}:"))
            Numbers.append(val)
            break
        except ValueError:
               print("invalid input.please enter a valid number")


largest=max(Numbers)
print(f"The largest number is:,{largest}")
