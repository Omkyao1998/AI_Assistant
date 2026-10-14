# Jarvis: Voice AI Assistant (Python + OpenAI)

A voice assistant you talk to through your microphone. It turns your speech into text, works out what kind of question you asked, sends it to an OpenAI model with a matching system prompt, and speaks the answer back. If it can't hear you, you can type instead.

## Why this project

Most chatbot demos answer every question in the same tone. I wanted an assistant that changes how it answers depending on the question: precise for technical questions, reflective for philosophical ones, calm for personal ones and structured for planning. It's a small, practical example of **prompt routing**, the same idea behind larger LLM applications.

## How it works

```
Microphone ──► Speech-to-text (Google Speech Recognition)
                   │
                   ▼
            Built-in commands? ── "time" ──► speaks the current time
                   │            ── "stop/exit" ──► says goodbye
                   ▼
            Context detection (keyword lists)
            technical · philosophical · strategic · personal · general
                   │
                   ▼
            System prompt for that context + your question ──► OpenAI Chat API
                   │
                   ▼
            Text-to-speech (pyttsx3) ──► Speaker
```

| Context | Example trigger words | Answer style |
|---|---|---|
| Technical | python, sql, power bi, docker, api | Clear, structured, precise |
| Philosophical | karma, dharma, consciousness, gita | Reflective |
| Strategic | plan, roadmap, deadline, stakeholder | Prioritised, long-term |
| Personal | stressed, motivation, career | Calm and understanding |

## Tech stack

Python · OpenAI Python SDK · SpeechRecognition · pyttsx3 · python-dotenv

## How to run

```bash
git clone https://github.com/Omkyao1998/AI_Assistant.git
cd AI_Assistant
pip install -r requirements.txt
cp .env.example .env        # then add your OpenAI API key to .env
python ai_assistant.py
```

Say something after **"Listening..."** appears. Say **"stop"** or **"exit"** to quit.

| Setting (.env) | Purpose |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI key (required) |
| `OPENAI_MODEL` | Model to use; set it to any current chat model |
| `SYSTEM_PROMPT` | Base personality of the assistant |

On Windows, if `PyAudio` fails to install, try `pip install pipwin && pipwin install pyaudio`.

## What I would improve next

- Match whole words instead of substrings for context detection (right now "ai" also matches "said")
- Keep conversation history so follow-up questions make sense
- Add more tools: weather, calendar, opening apps
- Stream the answer so speech starts sooner

## Author

**Omkar Gokhale** — Data Engineer & BI Analyst · [GitHub](https://github.com/Omkyao1998)
