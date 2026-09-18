Balance=100000

amount=float(input("Enter your withdrawal amount :"))

if amount<=Balance:
    print("withdrawal successful")
else:
    print("insufficient balance")