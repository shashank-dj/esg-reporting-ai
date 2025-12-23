import openai
import os

class OpenAILLMClient:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an ESG expert."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
