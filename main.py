from fastapi import FastAPI
from pydantic import BaseModel
from classify_emergency import classify_emergency
import sqlite3

app = FastAPI()


# This describes what data we expect to receive from the app
class EmergencyInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Backend is running!"}


@app.post("/analyze")
def analyze_emergency(input: EmergencyInput):

    # STEP A: Ask the classifier which emergency this is
    emergency_id = classify_emergency(input.text)

    # If the emergency was not recognized
    if emergency_id == "UNKNOWN":
        return {
            "emergency_id": "UNKNOWN",
            "message": "Emergency type could not be identified."
        }

    # STEP B: Connect to the emergency database
    conn = sqlite3.connect("emergencies.db")
    cursor = conn.cursor()

    # STEP C: Find the emergency in the database
    cursor.execute("""
        SELECT emergency_id, name, priority, procedure, checklist
        FROM emergencies
        WHERE emergency_id = ?
    """, (emergency_id,))

    result = cursor.fetchone()

    # Close the database
    conn.close()

    # If nothing was found
    if result is None:
        return {
            "emergency_id": emergency_id,
            "message": "Emergency was classified but not found in database."
        }

    # STEP D: Send database information back
    return {
        "emergency_id": result[0],
        "emergency_name": result[1],
        "priority": result[2],
        "procedure": result[3],
        "checklist": result[4]
    }


# STEP 10 - Incident Log

class IncidentInput(BaseModel):
    emergency_id: str
    time: str
    status: str
    completed_steps: list


@app.post("/incident")
def log_incident(input: IncidentInput):
    # For now, just confirm it was received
    # Later this can save to a file or database
    return {
        "message": "Incident logged",
        "data": input
    }


# Mission Control Update

@app.post("/mission-control/update")
def mission_control_update():
    return {
        "message": "Emergency Update",
        "details": "Emergency procedure initiated. Current status: Monitoring."
    }