# utils.py

import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key: {openai.api_key}")
def generate_ai_response(user, data):
    # prompt = f"Hello, {user.username}. Here is your health data: {data}. Can you provide some personalized advice and analysis?"
    # response = model(prompt, max_length=20)  # You can adjust max_length
    # return response[0]['generated_text']
    print(data, "data send to the ai")
    try:
        
        prompt = f"""
        you are a health assistant providing personalized feedback. Based on the following data, generate a friendly and motivational message for the user.

        User: {user}
        Data: {data}
        """
        response = openai.ChatCompletion.create(

            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a health advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"AI generation faild: {str(e)}"
