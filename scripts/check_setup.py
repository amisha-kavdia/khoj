import os
from dotenv import load_dotenv

load_dotenv()
key=os.getenv("GOOGLE_API_KEY")
print("Key loaded:",bool(key),"| length:", len(key) if key else 0)

import pandas,numpy,faiss,bm25s,sentence_transformers
print("Great ! All libraries imported fine.")