# utils.py

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_ai_response(user, data):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a health advisor."},
            {"role": "user", "content": f"Hello, {user.username}. Here is your health data: {data}. Can you provide some personalized advice and analysis?"}
        ]
    )
    return response.choices[0].message['content']
