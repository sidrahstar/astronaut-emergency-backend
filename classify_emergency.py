EMERGENCY_KEYWORDS = {
    "E001": ["pressure", "dropping", "decreasing", "falling", "low"],
    "E002": ["smoke", "fire", "burning", "burn"],
    "E003": ["communication", "contact", "link", "lost", "down"],
    "E004": ["equipment", "malfunction", "not responding", "stopped", "device"]
}

def classify_emergency(text):
    text_lower = text.lower()
    scores = {}

    for emergency_id, keywords in EMERGENCY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text_lower:
                score += 1
        scores[emergency_id] = score

    best_match = max(scores, key=scores.get)

    if scores[best_match] == 0:
        return "UNKNOWN"

    return best_match