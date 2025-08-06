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