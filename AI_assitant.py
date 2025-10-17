from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import datetime
import time
import random 
from dotenv import load_dotenv, find_dotenv
import os

#Initialise Env
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("API Key Loaded:", os.getenv("OPENAI_API_KEY")) #To check if right key is loading

#Initialise Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',175)

#Speech Output function
def speak(text):
    print('Jarvis: ',text)
    engine.say(text)
    engine.runAndWait()
	
#Listening Function
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en-in")
        print(f"You said: {query}\n")
    except Exception as e:
        speak("Sorry, I didn't catch that. Please repeat.")
        return ""
    return query.lower()

# AI Build Function
def build_prompt(context = "general"):
    base_prompt = """HOW YOU WANT YOUR AI TO THINK OR ACT"""
    
    if context == "technical":
        base_prompt += "\nFocus more on clarity, structure, and precision in technical reasoning."
    elif context == "philosophical":
        base_prompt += "\nBe more reflective and connect ideas to consciousness, dharma, and balance."
    elif context == "personal":
        base_prompt += "\nSpeak calmly and with compassion — be logical but understanding."
    elif context == "strategic":
        base_prompt += "\nFocus on decision-making, prioritization, and long-term planning."
    return base_prompt
	
#Asking Prompt
def ask_jarvis(prompt):
    #Keyword based context detection
    technical_keywords = [
    # Programming & Languages
    "python", "java", "c++", "javascript", "sql", "html", "css", "react", "node", "typescript",
    "rust", "go", "swift", "kotlin", "program", "coding", "developer", "script",
    "function", "variable", "loop", "class", "object", "debug", "syntax", "runtime",
    # Data & Analytics
    "data", "dataset", "database", "sql query", "dataframe", "csv", "excel", "power bi",
    "visualization", "dashboard", "analytics", "etl", "pipeline", "big data",
    "statistics", "regression", "forecasting", "kpi", "metric",
    # Machine Learning & AI
    "ai", "machine learning", "deep learning", "neural network", "nlp", "model",
    "training", "testing", "inference", "accuracy", "embedding", "clustering",
    "classification", "regression", "transformer", "llm", "prompt", "fine-tune",
    # Cloud & Infra
    "azure", "aws", "gcp", "docker", "kubernetes", "cloud", "vm", "deployment",
    "devops", "ci/cd", "terraform", "infrastructure", "compute", "server", "api",
    "endpoint", "microservice", "container", "storage",
    # Tech Topics
    "blockchain", "cryptography", "encryption", "quantum", "robotics",
    "automation", "script", "algorithm", "performance", "optimization",
    "scalability", "latency", "bug", "error", "exception", "test case"
    ]
    philosophical_keywords = ["life", "karma", "purpose", "truth", "mind", "soul", "spirit", "energy",
    "consciousness", "awareness", "reality", "illusion", "maya", "moksha",
    "enlightenment", "peace", "suffering", "desire", "ego", "wisdom", "virtue",
    "ethics", "morality", "self", "being", "existence", "reincarnation",
    "balance", "duality", "destiny", "fate", "universe", "creation", "death",
    "rebirth", "freedom", "detachment", "meditation", "bhakti", "dharma",
    "gita", "vedas", "upanishads", "vedanta", "yoga", "prana", "atman", "brahman",
    "truth", "contemplation", "nirvana", "awaken", "mindfulness", "inner peace"]

    personal_keywords = [ "feel", "sad", "happy", "angry", "tired", "stressed", "depressed", "anxious",
    "lonely", "worried", "confused", "lost", "fear", "hurt", "pain", "regret",
    "hope", "love", "relationship", "friend", "family", "career", "job", "life goal",
    "success", "failure", "motivation", "confidence", "discipline", "focus",
    "mindset", "mental health", "self-improvement", "insecurity", "rejection",
    "breakup", "trust", "patience", "calm", "overthinking", "jealous", "anger",
    "guilt", "acceptance", "growth", "self-doubt", "fear of failure", "tension",
    "peace", "forgive", "burnout", "stress relief"]

    strategic_keywords = ["plan", "strategy", "roadmap", "timeline", "milestone", "goal", "objective",
    "vision", "mission", "priority", "decision", "leadership", "management",
    "risk", "project", "team", "delegate", "execute", "schedule", "resource",
    "efficiency", "organization", "coordination", "meeting", "review",
    "deadline", "budget", "cost", "benefit", "impact", "progress", "deliverable",
    "kpi", "okr", "productivity", "performance", "problem solving",
    "negotiation", "stakeholder", "alignment", "strategy", "implementation",
    "scaling", "growth", "innovation", "vision", "long-term", "planning"]

    if any(word in prompt.lower() for word in technical_keywords):
        context = "technical"
    elif any(word in prompt.lower() for word in philosophical_keywords):
        context = "philosophical"
    elif any(word in prompt.lower() for word in strategic_keywords):
        context = "strategic"
    elif any(word in prompt.lower() for word in personal_keywords):
        context = "personal"
    else:
        context = "general"

    system_prompt = build_prompt(context)

    response = openai_client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[{"role":"system","content":system_prompt},{"role":"user","content":prompt}]
)
    return response['choices'][0]['message']['content']

def main():
    speak("Hello User, I am Jarvis. How may I assist you today?")
    print("Jarvis is listening.... say something (or type instead)")

    while(True):
        try:
            query = listen()

            if not query or query.strip() == "":
                query = input("Please Type instead: ").strip().lower()

            if not query:
                continue

            print(f"You said: {query}")

            # Exit condition
            if any(word in query.split() for word in ["stop", "exit", "quit", "goodbye"]):
                speak("Good Bye, Have a great day ahead")
                break
            # Time Check
            elif 'time' in query:
                strTime = datetime.datetime.now().strftime("%H%M%S")
                speak(f"The time is {strTime}")
            # Default ask
            else:
                response = ask_jarvis(query)
                print(f"Jarvis: {response}")
                speak(response)
        
            time.sleep(1) #small delay between response

        except Exception as e:
            print(f"Error:{e}")
            speak("Sorry, I encountered an error")


if __name__ == "__main__":
    main()
    
            