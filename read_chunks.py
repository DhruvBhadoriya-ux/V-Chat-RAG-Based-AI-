import requests
import os
import json
import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib 

def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )
    return r.json()['embeddings']


jsons = os.listdir("jsons") # List all the jsons 

my_dicts = []
chunk_id = 0
for json_file in jsons:
    if not json_file.endswith(".json"):
        continue

    file_path = f"jsons/{json_file}"

    # Skip empty files
    if os.path.getsize(file_path) == 0:
        print(f"Skipping empty file: {json_file}")
        continue

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        print(f"Creating Embeddings for {json_file}")
        embeddings = create_embedding([c['text'] for c in content['chunks']])

        for i, chunk in enumerate(content.get("chunks", [])):
            chunk["chunk_id"] = chunk_id
            chunk["embedding"] = embeddings[i]
            chunk_id += 1
            my_dicts.append(chunk)
    except json.JSONDecodeError:
        print(f"Invalid JSON format in: {json_file}")
        continue

    
#print(my_dicts)

df = pd.DataFrame.from_records(my_dicts)
#save this dataframe 
joblib.dump(df, 'embeddings.joblib')