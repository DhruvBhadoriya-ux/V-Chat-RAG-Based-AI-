import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib 
import requests
import streamlit as st 

def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3", 
            "input": text_list
        }
    )
    return r.json()['embeddings']

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate",json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    """response = r.json()
    print(response)
    return response"""
    response = r.json()["response"]
    #print("\nAI Answer:\n")
    #print(response)
    return response
df = joblib.load('embeddings.joblib')

incoming_query = input("Ask a Question: ")
    
question_embedding = create_embedding([incoming_query])[0]

# Find similarities of question embeddings with other embeddings 
# print(np.vstack(df.[embedding].values))
# print(np.vstack(df.[embedding]).shape)
embeddings_matrix = np.array(df['embedding'].tolist())
similarities = cosine_similarity(embeddings_matrix, [question_embedding]).flatten()
#print(similarities)
max_indx = similarities.argsort()[-5:][::-1]
#print(max_indx)
new_df = df.loc[max_indx]
#print(new_df[["title", "number", "text"]])

#==========================formatting timestamps=======================
def format_time(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"
    
new_df["start_time"] = new_df["start"].apply(format_time)
new_df["end_time"] = new_df["end"].apply(format_time)

#==========================prompt=============================
"""prompt = f'''I am teaching HTML, SEO and core web vitals in HTML.Here are video subtitle 
chunks containing video title, video number, start time in seconds,end time in seconds, 
the text at that time :

{new_df[["title", "number","start","end", "text"]].to_json(orient="records")}
------------------------------------
"{incoming_query}"

user asked this question related to video chunks, you have to answer in human way (dont mention the 
above format it just for you) where and how much content is taught in which video (in which video 
and at what timestamp) and guide the user to go to that particular video. If user asked unrelated 
question, tell him that you can only answer question related to the course.
'''"""

prompt = f"""
You are an AI assistant helping students navigate an HTML course.

Below are subtitle chunks from course videos including:
video title, video number, start time, end time, and text.

Context:
{new_df[["title","number","start_time","end_time","text"]].to_json(orient="records")}

Student Question:
{incoming_query}

Instructions:
- Answer naturally like a helpful AI tutor.
- Tell the student which video contains the answer.
- Mention the approximate timestamp where the topic is discussed.
- Explain briefly what is taught there.
- If the question is unrelated to the course, politely say you can only answer course-related questions.

Give a clear and helpful answer.
"""

with open ("prompt.txt", "w") as f:
    f.write(prompt)

"""response = inference(prompt)["response"]

with open ("response.txt", "w") as f:
    f.write(response)"""
response = inference(prompt)

with open("response.txt", "w") as f:
    f.write(response)

"""#====================GPT ANIMATION==========================
import time

placeholder = st.empty()
text = ""

for word in response.split():
    text += word + " "
    placeholder.write(text)
    time.sleep(0.05)

#====================X==================X====================="""
print("\n" + "="*50)
print("eduRAG-AI ASSISTANT")
print("="*50 + "\n")

print(response)

print("\n" + "="*50)
#for index, item in new_df.iterrows():
#    print(index,item["title"],item["number"], item["text"], item["start"],item["end"])

"""#========================CHAT-HISTORY========================
chat_history = []

chat_history.append({"role":"user","content":incoming_query})
chat_history.append({"role":"assistant","content":response})
#print("History:",chat_history)

#=============X=============================X================"""