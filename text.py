import speech_recognition as sr
import pyttsx3
import openai

engine = pyttsx3.init()

#function to capture user speech input
def get_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        print(f"You: {query}")
        return query
    except Exception as e:
        print(e)
        return None

#function to generate AI response
def generate_response(query, context):
    # Set up  OpenAI API client
    openai.api_key = "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"

    if "first question" in query.lower():
        first_question = context.split("User: ")[1].split("\n")[0]
        return first_question

    # Generate the response using OpenAI API
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"{context}User: {query}\nAI:",
        max_tokens=60,
        n=1,
        stop="User:",
        temperature=0.7,
    )

    # Extract the generated text from the response
    generated_text = response.choices[0].text.strip()

    # Check if the generated text is empty or contains an error message
    if not generated_text or "error" in generated_text.lower():
        return "Speak again."
    generated_text = generated_text.replace("User:", "").replace(query, "").strip()
    return generated_text

# Define the function to speak the AI response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Start the conversation
context = ""
speak("Hi, Welcome, how can I help you today?")
while True:
    query = get_input()
    if query:
        if "exit" in query.lower():
            speak("ThankYou, Goodbye!")
            break
        response = generate_response(query, context)
        context += f"User: {query}\nAI: {response}\n"
        print(f"AI: {response}")
        speak(response)
    else:
        speak("Sorry, I couldn't understand you. Please try again.")
