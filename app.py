from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import re

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def extract_field(label, text):
    pattern = rf"{label}:\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

@app.route('/generate', methods=['POST'])
def generate_alter_ego():
    data = request.json
    traits = data.get("traits", "")

    prompt = f"""
You are an AI character designer that creates deep, realistic alter egos for people based on their personality traits.

Create one believable alter ego for someone with these traits: {traits}.
This should feel like a real person with a full backstory, not a joke or parody.

Give the result in the following format:

Name: [Full realistic name]  
Occupation: [Plausible modern or historical profession]  
Origin: [City or region, country]  
Personality: [3 descriptive traits that sound human]  
Catchphrase: "[Something they often say that reveals their mindset or values]"  
Bio: [2–3 sentence life story that hints at both their strength and struggles. Make it cinematic but realistic.]

Now generate one for the given traits.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json={
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7  # Less random, more grounded
        }
    )

    text = response.json()["choices"][0]["message"]["content"]

    result = {
        "name": extract_field("Name", text),
        "occupation": extract_field("Occupation", text),
        "origin": extract_field("Origin", text),
        "personality": extract_field("Personality", text),
        "catchphrase": extract_field("Catchphrase", text).strip('"'),
        "bio": extract_field("Bio", text)
    }

    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
