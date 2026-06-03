import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import memory, DEVELOPER_ID, GROQ_MODEL
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve_memories(bug_description: str, bug_type: str) -> list:
    try:
        results = memory.search(
            query=f"{bug_type}: {bug_description}",
            filters={"user_id": DEVELOPER_ID},
            limit=3
        )
        hits = results.get("results", [])
        return hits
    except Exception as e:
        print(f"Memory retrieval failed: {e}")
        return []


def extract_principle(bug: str, suggested_fix: str, edit: str) -> str:
    try:
        prompt = (
            f"Bug: {bug[:100]}\n"
            f"AI fix: {suggested_fix[:150]}\n"
            f"Engineer changed to: {edit[:150]}\n"
            f"In one sentence, what coding preference does this reveal?"
        )
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Principle extraction failed: {e}")
        return f"Developer preferred this approach for {bug[:100]}: {edit[:200]}"


def save_memory(bug: str, bug_type: str, action: str,
                suggested_fix: str, reason: str = None,
                edited: str = None, principle: str = None):
    try:
        if action == "a":  # accept
            mem_text = (
                f"For {bug_type} bugs, this fix approach was accepted: "
                f"{suggested_fix[:300]}"
            )
        elif action == "r":  # reject
            mem_text = (
                f"For {bug_type} bugs, avoid this approach: "
                f"{suggested_fix[:200]}. Reason: {reason}"
            )
        elif action == "e":  # edit
            # Store the extracted principle, not the raw edit
            mem_text = principle or (
                f"For {bug_type} bugs, preferred style: {edited[:300]}"
            )
        elif action == "s":  # steer
            mem_text = (
                f"For {bug_type} bugs, engineer prefers this direction: {reason}"
            )
        else:
            return

        memory.add(
            messages=[{"role": "user", "content": mem_text}],
            user_id=DEVELOPER_ID,
            metadata={
                "action": action,
                "bug_type": bug_type
            },
            infer=False
        )
        print(f"Memory saved for action: {action}")

    except Exception as e:
        print(f"Memory save failed: {e}")


def get_all_memories() -> list:
    try:
        results = memory.get_all(filters={"user_id": DEVELOPER_ID})
        return results.get("results", [])
    except Exception as e:
        print(f"Failed to get all memories: {e}")
        return []