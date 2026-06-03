import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SESSION_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sessions.json")


def _load_sessions() -> list:
    if os.path.exists(SESSION_LOG):
        try:
            with open(SESSION_LOG, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_sessions(data: list):
    with open(SESSION_LOG, "w") as f:
        json.dump(data, f, indent=2)


def get_next_session_id() -> int:
    sessions = _load_sessions()
    if not sessions:
        return 1
    return max(s["session_id"] for s in sessions) + 1


def log_session(session_id: int, bug_id: str, bug_type: str,
                memories_retrieved: int, avg_confidence: float,
                path: str, action: str, steering: str = None):
    if path == "autonomous" and action == "a":
        depth = "none"
    elif action == "a":
        depth = "light"
    elif action == "e":
        depth = "medium"
    elif action in ["r", "s"]:
        depth = "heavy"
    else:
        depth = "unknown"

    entry = {
        "session_id":           session_id,
        "bug_id":               bug_id,
        "bug_type":             bug_type,
        "memories_retrieved":   memories_retrieved,
        "avg_confidence":       round(avg_confidence, 3),
        "path":                 path,
        "engineer_action":      action,
        "intervention_depth":   depth,
        "auto_steering_used":   steering is not None,
        "fix_accepted":         action == "a",
        "timestamp":            datetime.now().isoformat()
    }

    sessions = _load_sessions()
    sessions.append(entry)
    _save_sessions(sessions)

    return entry

def get_sessions() -> list:
    return _load_sessions()


def get_stats() -> dict:
    sessions = _load_sessions()
    if not sessions:
        return {}

    total = len(sessions)
    autonomous = sum(1 for s in sessions if s["path"] == "autonomous")
    accepted = sum(1 for s in sessions if s["fix_accepted"])
    heavy = sum(1 for s in sessions if s["intervention_depth"] == "heavy")
    medium = sum(1 for s in sessions if s["intervention_depth"] == "medium")
    avg_conf = sum(s["avg_confidence"] for s in sessions) / total

    return {
        "total_sessions":    total,
        "autonomy_rate":     round(autonomous / total * 100, 1),
        "acceptance_rate":   round(accepted / total * 100, 1),
        "heavy_rate":        round(heavy / total * 100, 1),
        "medium_rate":       round(medium / total * 100, 1),
        "avg_confidence":    round(avg_conf, 3)
    }