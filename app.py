from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Must be set in Render

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

    result = response.json()
    alter_ego = result["choices"][0]["message"]["content"]
    return jsonify({"result": alter_ego})

if __name__ == '__main__':
    app.run(debug=True)
