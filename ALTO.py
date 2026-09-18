from fastapi import FastAPI
app = FastAPI()

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

@app.get("/students/{student_id}")
def get_students(student_id:int):
    return{
        "students_id":student_id
    }
