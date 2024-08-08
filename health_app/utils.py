# utils.py

import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
# print(f"API Key: {openai.api_key}")
def generate_ai_response(user, data, topic):
    try:

        prompt = f"""
        you are a health assistant providing personalized feedback. Based on the following data, generate a friendly and motivational message for the user.

        
        User: {user.username}
        Data: {data}
        topic: {topic}


        Example Response format:
        "Hello, [name]. I see that you walked [stepCount] steps today, which is 4,000 more than yesterday. It's great that you are so active! I noticed that on days when you walk a lot, you sleep 20% better. Keep it up and continue in the same spirit to reach your goal."
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
