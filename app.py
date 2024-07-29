from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator

app = Flask(__name__)

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def recognize_speech(language_code):
    with sr.Microphone() as source:
        print("Listening.....")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        print("Recognizing.....")
        query = recognizer.recognize_google(audio, language=language_code)
        print(f"The User said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio, please try again.....")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"

def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    input_language = request.form['input_language']
    output_language = request.form['output_language']
    text = request.form.get('text', '')

    if text:
        query = text
    else:
        query = recognize_speech(input_language)

    if query != "None":
        translated_text = translate_text(query, output_language)
        return jsonify({'query': query, 'translated_text': translated_text})
    else:
        return jsonify({'error': 'Speech recognition failed.'}), 400

if __name__ == '__main__':
    app.run(debug=True)