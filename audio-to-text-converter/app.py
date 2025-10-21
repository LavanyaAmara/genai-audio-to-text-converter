from flask import Flask, render_template, request, jsonify
import whisper
import os

app = Flask(__name__)

# Load Whisper model once at startup
model = whisper.load_model("base")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    # Check if file is in the request
    if 'audio' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save the uploaded audio
    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(file_path)

    try:
        # Transcribe and translate to English
        result = model.transcribe(file_path, task="translate")
        text = result["text"]

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
