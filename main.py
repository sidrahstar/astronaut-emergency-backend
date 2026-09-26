from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from classify_emergency import classify_emergency
import sqlite3
import traceback

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# IMPORTANT: without this, an unhandled exception in any route returns a 500
# response with NO CORS headers attached (a known FastAPI/Starlette quirk).
# The browser then reports it as a "CORS error" instead of showing the real
# server error, which is what was happening here. This handler makes sure
# errors are returned as normal JSON responses (with CORS headers intact)
# so the real cause shows up in the browser console / Network tab instead.
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()  # so you can see the real error in Render's logs
    return JSONResponse(
        status_code=500,
        content={"detail": f"{type(exc).__name__}: {exc}"},
    )

# This describes what data we expect to receive from the app
class EmergencyInput(BaseModel):
    emergencyInput: str


@app.get("/")
def home():
    return {"message": "Backend is running!"}


@app.post("/analyze")
def analyze_emergency(input: EmergencyInput):

    # STEP A: Ask the classifier which emergency this is
    emergency_id = classify_emergency(input.emergencyInput)

    # If the emergency was not recognized
    if emergency_id == "UNKNOWN":
        return {
            "emergency_id": "UNKNOWN",
            "message": "Emergency type could not be identified."
        }

    # STEP B: Connect to the emergency database
    # check_same_thread=False avoids issues under FastAPI's async workers;
    # sqlite3.connect() does NOT error if the file/table is missing, so we
    # verify the table exists rather than letting a bad query crash silently.
    conn = sqlite3.connect("emergencies.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='emergencies'
    """)
    if cursor.fetchone() is None:
        conn.close()
        return {
            "emergency_id": emergency_id,
            "message": (
                "Database is missing the 'emergencies' table. "
                "Check that emergencies.db was committed to the repo and "
                "deployed alongside the backend."
            ),
        }

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