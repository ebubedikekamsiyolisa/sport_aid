from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "welcome to my API"}


@app.post("/students")
def create_students(name:str,age:int,course:str):
    return{
         "Message":"students Added sucessfully",
         "students":{
         "name":name,
         "age":age,
         "course":course
    }

    }