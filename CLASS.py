from fastapi import FastAPI

app = FastAPI()

app.get("/")
def home():
    return{"message":"welocome to my API"}


@app.post("/students")
def create_students(name: str, age: int,gender:str,address:str, course: str):
    return{
        "message":"students added successfully",
        "students":{
        "name":name,
        "age":age,
        "gender":gender,
        "address":address,
        "course":course
        }
        }