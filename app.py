from flask import Flask, render_template, request, send_file, url_for, send_from_directory, redirect
import os
import shutil
from backend import encode_phase, decode_phase
import wave
import numpy as np

app = Flask(__name__)


def text_to_binary(text):
    # Convert text to binary
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    # Convert binary to text
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

# Define other functions like encode_phase and decode_phase here


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    text = request.form['text']
    audio_file = request.files['audio']
    audio_file.save(os.path.join(app.root_path, 'input_audio.wav'))

    binary_text = text_to_binary(text)
    encode_phase('input_audio.wav', binary_text)

    # Move the encrypted audio file to the "encrypted_audios" folder
    encrypted_audio_path = os.path.join(app.root_path, 'encrypted_audios')
    os.makedirs(encrypted_audio_path, exist_ok=True)
    encrypted_audio_file = os.path.join(
        encrypted_audio_path, 'encrypted_audio.wav')
    shutil.move('encrypted_audio.wav', encrypted_audio_file)

    return 'Encryption done! <a href="/download">Download Encrypted Audio</a>'


@app.route('/download')
def download():
    return send_from_directory(app.root_path, 'encrypted_audios/encrypted_audio.wav', as_attachment=True)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    audio_file = request.files['encrypted_audio']
    audio_file.save(os.path.join(app.root_path, 'encrypted_audio.wav'))

    decoded_binary = decode_phase('encrypted_audio.wav')
    decoded_text = binary_to_text(decoded_binary)

    return render_template('result.html', decryption_result=decoded_text)


if __name__ == '__main__':
    app.run(debug=True)
