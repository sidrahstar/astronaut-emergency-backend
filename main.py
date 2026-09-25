from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# This describes what data we expect to receive from the app
class EmergencyInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.post("/analyze")
def analyze_emergency(input: EmergencyInput):
    astronaut_text = input.text

    emergency_id = "E001"

    result = {
        "emergency_id": emergency_id,
        "emergency_name": "Cabin Pressure",
        "priority": "Critical",
        "procedure": "placeholder procedure text",
        "checklist": ["Step 1", "Step 2", "Step 3", "Step 4"]
    }

    return result