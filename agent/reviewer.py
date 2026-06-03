import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def show_fix(bug_description: str, fix: str, confidence_label: str,
             path: str, steering: str = None):
    print("\n" + "=" * 60)
    print(" DEBUG AGENT")
    print("=" * 60)
    print(f"Bug:        {bug_description}")
    print(f"Path:       {path.upper()}  |  Confidence: {confidence_label}")
    if steering:
        print(f"\nAuto-steering applied:\n{steering}")
    print(f"\nProposed Fix:\n{fix}")
    print("=" * 60)


def get_feedback() -> dict:
    print("\nYour options:")
    print("  [a] Accept - fix is good as-is")
    print("  [r] Reject - wrong approach")
    print("  [e] Edit   - partially right, you'll correct it")
    print("  [s] Steer  - redirect before fix is applied")

    while True:
        action = input("\nYour choice (a/r/e/s): ").strip().lower()
        if action in ["a", "r", "e", "s"]:
            break
        print("Invalid choice. Please enter a, r, e, or s.")

    result = {"action": action, "reason": None, "edited": None}

    if action == "r":
        result["reason"] = input("Why are you rejecting? Brief reason: ").strip()

    elif action == "e":
        print("Paste your corrected version.")
        print("Press Enter twice when done:")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        result["edited"] = "\n".join(lines)

    elif action == "s":
        result["reason"] = input("What direction should the fix take? ").strip()

    return result


def show_session_summary(session_id: int, path: str,
                         action: str, confidence: float,
                         memories_used: int):
    action_labels = {"a": "Accepted", "r": "Rejected", "e": "Edited", "s": "Steered"}
    print(
        f"\nSession {session_id} complete | "
        f"Path: {path.upper()} | "
        f"Action: {action_labels.get(action, action)} | "
        f"Confidence: {confidence:.2f} | "
        f"Memories used: {memories_used}"
    )
