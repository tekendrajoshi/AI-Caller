# AI-Caller

people can call the ai agent and talk to that from phone.

WORKFLOW :
User calls a Twilio number
⬇️
Twilio receives call and streams audio in real-time
⬇️
Audio is sent to Whisper (OpenAI) → Speech-to-Text (STT)
⬇️
Transcribed text sent to OpenAI (ChatGPT/GPT-4o) → Generates response
⬇️
Response text sent to ElevenLabs API → Text-to-Speech (TTS)
⬇️
Generated audio returned to Twilio → Played back to the caller
