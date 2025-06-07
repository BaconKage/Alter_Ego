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
You are an AI that creates wild, eccentric alter egos based on personality traits.

Create one fictional alter ego for someone with these traits: {traits}.
Give the result in the following format:

Name: [full fictional name]
Occupation: [job title]
Origin: [country or planet]
Personality: [3 traits]
Catchphrase: "[funny or dramatic quote]"
Bio: [2-line description]

Make it unexpected, creative, and slightly absurd.
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
            "temperature": 0.95
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
