import json
import os
import urllib.parse
import urllib.request
from groq import Groq
from app.services.meal_db import search_meals


client = Groq(

    api_key=os.environ.get("GROQ_API_KEY"),

)
recipe = search_meals

chat_completion = client.chat.completions.create(

    messages=[

        {

            "role": "user",

            "content": "Explain how to make the following recipe: " + recipe ,

        }

    ],

    model="llama-3.3-70b-versatile",

)


print(chat_completion.choices[0].message.content)