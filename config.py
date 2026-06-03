import os
from dotenv import load_dotenv
from mem0 import Memory
import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("mem0").setLevel(logging.ERROR)

load_dotenv()

# Validate all keys are present
required_keys = [
    "GROQ_API_KEY",
    "QDRANT_URL",
    "QDRANT_API_KEY"
]

for key in required_keys:
    if not os.getenv(key):
        raise ValueError(f"Missing environment variable: {key}")

mem0_config = {
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "multi-qa-MiniLM-L6-cos-v1",
            "embedding_dims": 384
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": os.getenv("QDRANT_URL"),
            "api_key": os.getenv("QDRANT_API_KEY"),
            "collection_name": "debug_agent",
            "embedding_model_dims": 384
        }
    },
    "llm": {
        "provider": "groq",
        "config": {
            "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            "api_key": os.getenv("GROQ_API_KEY")
        }
    }
}

memory = Memory.from_config(mem0_config)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.80))
DEVELOPER_ID = os.getenv("DEVELOPER_ID", "dev_01")

print("Config loaded successfully")
print(f"Confidence threshold: {CONFIDENCE_THRESHOLD}")
print(f"Developer ID: {DEVELOPER_ID}")