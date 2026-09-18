main_text="software development is fun"

sub_string=str(input("enter a sub_string:"))

if sub_string in main_text:
    print(f"yes,'{sub_string}' is present in text")
else:
    print(f"no,'{sub_string}' is absent in text")