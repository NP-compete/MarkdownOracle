import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    return {
        "REPO_URL": os.getenv("REPO_URL"),
        "EMBEDDING_MODEL": os.getenv("EMBEDDING_MODEL"),
        "BASE_URL": os.getenv("BASE_URL"),
        "MODEL_NAME": os.getenv("MODEL_NAME"),
    }
