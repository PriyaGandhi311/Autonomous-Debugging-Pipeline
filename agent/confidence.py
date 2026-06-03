import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import CONFIDENCE_THRESHOLD


def compute_confidence(memories: list) -> float:
    if not memories:
        return 0.0

    scores = [m["score"] for m in memories]
    avg_score = sum(scores) / len(scores)

    strong_memories = [s for s in scores if s > 0.60]
    if len(strong_memories) >= 3:
        avg_score = min(avg_score + 0.10, 1.0)

    return round(avg_score, 3)


def should_act_autonomously(confidence: float) -> bool:
    return confidence >= CONFIDENCE_THRESHOLD


def confidence_label(confidence: float) -> str:
    if confidence >= 0.80:
        return f"HIGH ({confidence:.2f}) - acting autonomously"
    elif confidence >= 0.50:
        return f"MEDIUM ({confidence:.2f}) - showing fix, needs review"
    else:
        return f"LOW ({confidence:.2f}) - needs engineer guidance"