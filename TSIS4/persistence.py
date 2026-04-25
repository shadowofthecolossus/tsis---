import json
import os

# load or create settings
def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            return json.load(f)
    return {"sound": True, "color": "blue", "diff": "normal"}

# save settings
def save_settings(data):
    with open('settings.json', 'w') as f:
        json.dump(data, f)

# load top scores
def load_leaderboard():
    if os.path.exists('leaderboard.json'):
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    return []

# save new score and keep top 10
def save_score(name, score, dist):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "dist": int(dist)})
    # sort by score
    lb = sorted(lb, key=lambda x: x["score"], reverse=True)[:10]
    with open('leaderboard.json', 'w') as f:
        json.dump(lb, f)