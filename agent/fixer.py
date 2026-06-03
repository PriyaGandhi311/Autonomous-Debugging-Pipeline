import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from config import GROQ_MODEL

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_fix(code: str, bug_description: str, memories: list) -> str:
    memories = memories[:3]
    memory_context = (
        "\n".join([f"- {m['memory']}" for m in memories])
        if memories else "No prior preferences on record."
    )

    prompt = f"""
    You are an expert Python debugging assistant.
    Developer preferences from past sessions:
    {memory_context}
    Bug description: {bug_description}
    Buggy code:
    {code}
    Propose a fix that respects the developer's preferences above.
    Return your response in this exact format:
    EXPLANATION:
    <brief explanation of what the bug is and how you are fixing it>
    FIXED CODE:
    <complete corrected code>
    """
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()