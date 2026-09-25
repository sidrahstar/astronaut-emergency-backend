from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/emergency/{emergency_id}")
def get_emergency(emergency_id: str):

    conn = sqlite3.connect("emergencies.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM emergencies WHERE emergency_id = ?",
        (emergency_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"error": "Emergency not found"}

    return {
        "emergency_id": row[0],
        "name": row[1],
        "priority": row[2],
        "keywords": row[3],
        "procedure": row[4],
        "checklist": row[5]
    }