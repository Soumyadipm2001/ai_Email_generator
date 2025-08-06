# Main.py

from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv
from werkzeug.wrappers import response

load_dotenv()
GROQ_API_KEY = os.getenv("AI_email")

app = Flask(__name__)

client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_response', methods=['POST'])
def generate_email():
    data = request.get_json()
    topic = data.get("topic","")
    tone = data.get("tone","formal")
    receiver = data.get("receiver","hr@gmail.com")


    prompt = f"Write an {tone} email to {receiver} about: {topic}"

    try:
        response = client.chat.completions.create(model="llama3-70b-8192", messages=[{"role": "system", "content": "You are an expert email assistant."},{"role": "user", "content": prompt}])


        email_text = response.choices[0]. message.content
        return jsonify({"email": email_text})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
  app.run(debug=True)

  # Index.html

  <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI Email Generator</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f4f4f4;
      padding: 40px;
      color: #333;
      text-align: center;
    }

    h1 {
      color: #2c3e50;
    }

    form {
      background: #fff;
      padding: 25px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      max-width: 500px;
      margin: 0 auto 30px;
    }

    label {
      font-weight: bold;
      display: block;
      margin-bottom: 5px;
      text-align: left;
    }

    input, select {
      width: 100%;
      padding: 10px;
      margin-bottom: 20px;
      border-radius: 5px;
      border: 1px solid #ccc;
      font-size: 16px;
    }

    button {
      padding: 12px 20px;
      background-color: #3498db;
      color: #fff;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
    }

    button:hover {
      background-color: #2980b9;
    }

    pre {
      background: #ecf0f1;
      padding: 20px;
      border-radius: 10px;
      white-space: pre-wrap;
      word-wrap: break-word;
      max-width: 700px;
      margin: 0 auto;
      text-align: left;
      font-size: 16px;
    }
  </style>
</head>
<body>

  <h1>Generate Email with AI</h1>

  <form id="emailForm">
      <label for="receiver">Receiver:</label>
      <input type="text" id="receiver" placeholder="Sir/Madam">

      <label for="topic">Topic:</label>
      <input type="text" id="topic" placeholder="e.g., apology for late response">

      <label for="tone">Tone:</label>
      <select id="tone">
          <option value="formal">Formal</option>
          <option value="informal">Informal</option>
          <option value="friendly">Friendly</option>
      </select>

      <button type="submit">Generate Email</button>
  </form>

  <h1>Generated Email:</h1>
  <pre id="result"></pre>

  <script>
      document.getElementById('emailForm').addEventListener('submit', function(e) {
          e.preventDefault();

          fetch('/get_response', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                  receiver: document.getElementById('receiver').value,
                  topic: document.getElementById('topic').value,
                  tone: document.getElementById('tone').value,
              })
          })
          .then(res => res.json())
          .then(data => {
              if (data.email) {
                  document.getElementById('result').textContent = data.email;
              } else {
                  document.getElementById('result').textContent = "Error: " + data.error;
              }
        });
      });
  </script>

</body>
</html>
