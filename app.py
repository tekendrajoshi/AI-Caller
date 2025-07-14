from flask import Flask, request, send_file, jsonify
from openai import OpenAI
import requests
import tempfile

app = Flask(__name__)

# ✅ API Keys
OPENAI_API_KEY = 'API KEY OF OPEN AI'
ELEVENLABS_API_KEY = 'API KEY OF ELEVEN LABS'
ELEVENLABS_VOICE_ID = '4NejU5DwQjevnR6mh3mb'

client = OpenAI(api_key=OPENAI_API_KEY)

# ✅ Transcribe audio using Whisper
def transcribe_audio(file):
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.mp3", file.stream, "audio/mpeg")
    )
    return response.text

# ✅ Get GPT response
def get_gpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ✅ Convert text to speech using ElevenLabs
def elevenlabs_tts(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.6
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.content

# ✅ Flask endpoint
@app.route('/voice', methods=['POST'])
def voice_pipeline():
    try:
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({"error": "No audio file uploaded"}), 400

        user_text = transcribe_audio(audio_file)
        print("User said:", user_text)

        reply_text = get_gpt_response(user_text)
        print("GPT replied:", reply_text)

        audio_data = elevenlabs_tts(reply_text)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_data)
            temp_path = tmp.name

        return send_file(temp_path, mimetype="audio/mpeg")

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
