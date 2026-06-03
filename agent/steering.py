import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from config import GROQ_MODEL

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def autonomous_steer(bug: str, code: str, memories: list) -> tuple:
    memories = memories[:3]
    memory_text = "\n".join([f"- {m['memory']}" for m in memories])

    steering_prompt = f"""
    You are simulating an experienced engineer's judgment.
    Based on these developer preferences learned from past sessions:
    {memory_text}
    For this bug: {bug}
    What specific fix direction would this developer prefer?
    Be concrete, state exactly:
    - What pattern or approach to use
    - What to avoid
    - Why, based on their known preferences
    Respond in 2-3 sentences max. Be direct and specific.
    """
    steering_response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": steering_prompt}],
        max_tokens=200
    )
    steering = steering_response.choices[0].message.content.strip()

    fix_prompt = f"""
    You are an expert Python debugging assistant.
    Fix this bug following these directions exactly:
    {steering}
    Buggy code:
    {code}
    Return your response in this exact format:
    EXPLANATION:
    <brief explanation of what the bug is and how you are fixing it>
    FIXED CODE:
    <complete corrected code>
    """

    fix_response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": fix_prompt}],
        max_tokens=1000
    )
    fix = fix_response.choices[0].message.content.strip()

    return steering, fix