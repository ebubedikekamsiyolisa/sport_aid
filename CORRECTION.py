from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    id:int
    name: str
    age: int
    gender: str
    course: str
Mark= []


@app.get("/")
def home():
    return {"message": "Welcome to my API"}


@app.post("/students")
def add_student(student: Student):
    Mark.append(student)
    return {
        "Message": "students added sucessfully",
        "student": student

    }



@app.get("/students")
def get_students():
    return {
        "Total Students": len(Mark),
        "Students": Mark
    }


