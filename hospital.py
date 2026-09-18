from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

class Patient(BaseModel):
    id:int
    name: str
    age: int
    gender: str
    home_address: str
    phone_number: str
    ailments: str
Mark=[]


@app.get("/")
def home():
    return {"message": "Welcome to my API"}


@app.post("/patients")
def add_patient(patient:Patient):
    Mark.append(patient)
    return{
        "Message": "patient added sucessfully",
        "patient": patient

    }


@app.get("/patients")
def get_patients():
    return{
        "Total Patients": len(Mark),
        "Patients": Mark
    }




