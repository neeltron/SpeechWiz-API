from flask import Flask, request
import os
from google.cloud import speech
from pydub import AudioSegment

credential_path = "bruh.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

app = Flask('app')

def transcribe_file(speech_file: str) -> speech.RecognizeResponse:

    m4a_audio = AudioSegment.from_file(speech_file, format="m4a")
    m4a_audio.export("audio.mp3", format="mp3")
    client = speech.SpeechClient()

    with open("audio.mp3", "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        sample_rate_hertz=8000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    print(response)
    print("here")
    for result in response.results:
        print("here2")
        print(result)

    return response



@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/upload', methods = ["POST"])
def upload():
  if request.method == 'POST':
    file = request.files['file']
    print("req received")
    if file:
      print("file is there")
      file.save("audio.m4a")
      print(transcribe_file("audio.m4a"))
      return "upload successful!"
    else:
      return "no file"
  

app.run(host='0.0.0.0', port=8080)
