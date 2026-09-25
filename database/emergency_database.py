import sqlite3
import json

# Connect to the database
conn = sqlite3.connect("emergencies.db")
cursor = conn.cursor()

# Create the emergencies table if it does not already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS emergencies (
    emergency_id TEXT PRIMARY KEY,
    name TEXT,
    priority TEXT,
    keywords TEXT,
    procedure TEXT,
    checklist TEXT
)
""")

# Emergency information
emergencies = [
    {
        "emergency_id": "E001",
        "name": "Cabin Pressure",
        "priority": "Critical",
        "keywords": "pressure,dropping,decreasing,falling,low",
        "procedure": "Confirm cabin pressure decrease. Alert crew and Mission Control. Move crew to the designated safe area. Close hatches to isolate the affected section. Determine whether the leak is slow or rapid. Monitor pressure and locate the leak if conditions are safe. Apply an approved repair procedure if possible. Continue monitoring cabin pressure. If pressure cannot be stabilized, prepare for evacuation using the designated crew spacecraft.",
        "checklist": json.dumps([
            "Check cabin pressure readings",
            "Alert crew and Mission Control",
            "Move to designated safe area",
            "Close hatches and isolate affected section",
            "Determine leak rate",
            "Locate the leak if safe",
            "Apply approved repair procedure",
            "Monitor cabin pressure",
            "Prepare for evacuation if required"
        ])
    },

    {
        "emergency_id": "E002",
        "name": "Fire / Smoke",
        "priority": "Critical",
        "keywords": "fire,smoke,flames,overheating,burning smell",
        "procedure": "Confirm the fire or smoke indication. Alert all crew members and Mission Control. Identify the affected location if it is safe to do so. Isolate the affected area by closing the appropriate hatch or ventilation path. Shut down the affected equipment if safe. Use the approved onboard fire suppression equipment according to the emergency procedure. Monitor the atmosphere for smoke and hazardous gases. If the fire cannot be controlled, move the crew to a safe area and prepare for evacuation if required.",
        "checklist": json.dumps([
            "Confirm fire or smoke indication",
            "Alert crew and Mission Control",
            "Identify affected location if safe",
            "Isolate the affected area",
            "Shut down affected equipment if safe",
            "Use approved fire suppression equipment",
            "Monitor cabin atmosphere",
            "Move to safe area if necessary",
            "Prepare for evacuation if required"
        ])
    },

    {
        "emergency_id": "E003",
        "name": "Communication Failure",
        "priority": "Critical",
        "keywords": "communication,communications failure,no signal,radio failure,loss of contact",
        "procedure": "Confirm the communication failure and check the communication system status. Attempt communication using the primary communication system. If unsuccessful, switch to the approved backup communication system. Check associated equipment and connections if safe. Attempt to establish communication with Mission Control using the designated backup method. Follow the verified communication-loss procedure and maintain crew safety. Record the communication status and continue monitoring until normal communication is restored.",
        "checklist": json.dumps([
            "Confirm communication failure",
            "Check communication system status",
            "Attempt primary communication",
            "Switch to approved backup communication system",
            "Check equipment and connections if safe",
            "Attempt backup communication with Mission Control",
            "Follow communication-loss procedure",
            "Maintain crew safety",
            "Monitor until communication is restored"
        ])
    },

    {
        "emergency_id": "E004",
        "name": "Equipment Malfunction",
        "priority": "High",
        "keywords": "equipment failure,malfunction,fault,error,system failure,not working",
        "procedure": "Confirm the equipment malfunction and identify the affected system. Notify the crew and Mission Control. Check system status and available warnings or fault indicators. If safe, place the affected equipment in the approved safe configuration or switch to a backup system. Follow the verified troubleshooting procedure for the specific equipment. Monitor the affected system and cabin conditions. If the malfunction cannot be resolved, isolate the equipment and continue operations using the available backup system or contingency procedure.",
        "checklist": json.dumps([
            "Confirm equipment malfunction",
            "Identify affected system",
            "Notify crew and Mission Control",
            "Check system status and fault indicators",
            "Place affected equipment in safe configuration if required",
            "Switch to approved backup system if available",
            "Follow verified troubleshooting procedure",
            "Monitor the affected system",
            "Isolate equipment if necessary",
            "Continue using backup or contingency procedure"
        ])
    }
]

# Put the emergency information into the database
for e in emergencies:
    cursor.execute("""
    INSERT OR REPLACE INTO emergencies
    (emergency_id, name, priority, keywords, procedure, checklist)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        e["emergency_id"],
        e["name"],
        e["priority"],
        e["keywords"],
        e["procedure"],
        e["checklist"]
    ))

# Save everything
conn.commit()

# Close the database
conn.close()

print("Data inserted successfully!")