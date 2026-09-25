from fastapi import FastAPI
from pydantic import BaseModel
from classifier import
classify_emergency

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

    # STEP A: Ask P4's classifier which emergency this is
    # (we'll connect this properly once P4 shares their code)
    emergency_id = classify_emergency(astronaut_text)  # placeholder for now

    # STEP B: Ask P5/P1's database for the full details
    # (we'll connect this properly once P1/P5 share their code)
    result = {
        "emergency_id": emergency_id,
        "emergency_name": "Cabin Pressure",
        "priority": "Critical",
        "procedure": "placeholder procedure text",
        "checklist": [
            "Step 1",
            "Step 2",
            "Step 3",
            "Step 4"
        ]
    }

    return result