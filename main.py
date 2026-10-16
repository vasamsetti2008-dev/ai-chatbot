import ollama

print("AI Chatbot Started!")
print("Type 'exit' to stop.")

while True:
    message = input("You: ")

    if message.lower() == "exit":
        print("Bye bro!")
        break

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        print("AI:", response["message"]["content"])

    except Exception as e:
        print("Error:", e)