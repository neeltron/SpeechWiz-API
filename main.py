from flask import Flask, request
app = Flask('app')

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
      return "upload successful!"
    else:
      return "no file"
  

app.run(host='0.0.0.0', port=8080)
