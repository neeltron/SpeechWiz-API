from flask import Flask, request, jsonify, make_response
import os
from google.cloud import speech
from pydub import AudioSegment
import json
from google.protobuf.json_format import MessageToDict
from textblob import TextBlob

credential_path = "bruh.json" # i have not uploaded this file to github because it's my api key

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
      enable_automatic_punctuation = True
  )

  response = client.recognize(config=config, audio=audio)
  global transcribe
  # print(response)
  # print("here")
  global transcription_string
  transcription_string = ""
  transcribe = MessageToDict(response._pb)
  for result in transcribe['results']:
    # print("here2")
    transcription_string += result['alternatives'][0]['transcript']
    # print(result)
  print("Final String:", transcription_string)
  blob = TextBlob(transcription_string)
  print(blob.sentiment)
  global transcript
  transcript = {'text': transcription_string, 'polarity': 'something goes here', 'subjectivity': 'something goes here too'}
  if blob.sentiment.polarity < -0.5:
    transcript['polarity'] = 'negative'
  elif blob.sentiment.polarity > -0.6 and blob.sentiment.polarity < 0.2:
    transcript['polarity'] = 'slightly negative'
  elif blob.sentiment.polarity > -0.3 and blob.sentiment.polarity < 0.3:
    transcript['polarity'] = 'neutral'
  elif blob.sentiment.polarity > 0.2 and blob.sentiment.polarity < 0.6:
    transcript['polarity'] = 'slightly positive'
  else:
    transcript['polarity'] = 'positive'

  if blob.sentiment.subjectivity > 0.5:
    transcript['subjectivity'] = 'subjective'
  else:
    transcript['subjectivity'] = 'objective'
  
  return response


@app.route('/')
def hello_world():
  return 'Hello, World!'


@app.route('/upload', methods=["POST"])
def upload():
  if request.method == 'POST':
    file = request.files['file']
    print("req received")
    if file:
      print("file is there")
      file.save("audio.m4a")
      transcribe_file("audio.m4a")
      return "upload successful!"
    else:
      return "no file"


@app.route('/export', methods=["GET"])
def export():
  if request.method == 'GET':
    # print(transcribe)
    return make_response(transcript)
  else:
    return "not get"


app.run(host='0.0.0.0', port=8080)
