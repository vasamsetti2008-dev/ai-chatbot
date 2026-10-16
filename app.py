from flask import Flask, request, jsonify, render_template_string
import ollama

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>My AI Chatbot</title>
    <style>
        body {
            background: #101827;
            color: white;
            font-family: Arial;
            text-align: center;
            padding: 40px 15px;
        }
        .chat {
            max-width: 600px;
            margin: auto;
            background: #1e293b;
            padding: 24px;
            border-radius: 16px;
        }
        #messages {
            text-align: left;
            min-height: 180px;
            white-space: pre-wrap;
        }
        input {
            width: 68%;
            padding: 12px;
            border-radius: 8px;
        }
        button {
            padding: 12px;
            background: #38bdf8;
            border: 0;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="chat">
        <h1>🤖 My AI Chatbot</h1>
        <div id="messages">AI: Hello bro! Ask me anything.</div>
        <input id="msg" placeholder="Type your message...">
        <button onclick="send()">Send</button>
    </div>
    <script>
        async function send() {
            const input = document.getElementById('msg');
            const box = document.getElementById('messages');
            const text = input.value.trim();
            if (!text) return;

            box.textContent += '\\nYou: ' + text + '\\nAI: Thinking...';
            input.value = '';

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                box.textContent = box.textContent.replace(
                    'AI: Thinking...', 'AI: ' + data.reply
                );
            } catch (e) {
                box.textContent += '\\nCould not connect to AI.';
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message", "")
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": message}]
    )
    return jsonify({"reply": response["message"]["content"]})

if __name__ == "__main__":
    app.run(debug=True)