# utils.py

import openai
from django.conf import settings

from transformers import pipeline

# Load the model
model = pipeline('text-generation', model='gpt2') 

# openai.api_key = settings.OPENAI_API_KEY

def generate_ai_response(user, data):
    prompt = f"Hello, {user.username}. Here is your health data: {data}. Can you provide some personalized advice and analysis?"
    response = model(prompt, max_length=20)  # You can adjust max_length
    return response[0]['generated_text']




    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a health advisor."},
    #         {"role": "user", "content": f"Hello, {user.username}. Here is your health data: {data}. Can you provide some personalized advice and analysis?"}
    #     ]
    # )
    # return response.choices[0].message['content']
