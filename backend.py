import wave
import numpy as np


def text_to_binary(text):
    # Convert text to binary
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    # Convert binary to text
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))


def encode_phase(audio_file, binary_data):
    # Open audio file
    audio = wave.open(audio_file, mode='rb')
    params = audio.getparams()
    frames = audio.readframes(-1)
    audio.close()

    # Convert audio frames to numpy array and create a mutable copy
    frames = np.frombuffer(frames, dtype=np.int16)
    frames = frames.copy()

    # Convert binary data to array of 1s and -1s
    binary_array = np.array([1 if bit == '1' else -1 for bit in binary_data])

    # Encode binary data into audio frames by modifying phase
    frames_length = len(frames)
    binary_length = len(binary_array)
    for i in range(binary_length):
        frames[i % frames_length] += binary_array[i] * 100

    # Save the modified frames to a new audio file
    output_audio = wave.open('encrypted_audio.wav', 'wb')
    output_audio.setparams(params)
    output_audio.writeframes(frames.tobytes())
    output_audio.close()


def decode_phase(audio_file):
    # Open the encrypted audio file
    audio = wave.open(audio_file, mode='rb')
    frames = audio.readframes(-1)
    audio.close()

    # Convert audio frames to numpy array
    frames = np.frombuffer(frames, dtype=np.int16)

    # Extract binary data from audio frames
    decoded_data = []
    for frame in frames:
        if frame > 0:
            decoded_data.append('1')
        else:
            decoded_data.append('0')

    return ''.join(decoded_data)


# Example usage:
text = "Hello, world!"
binary_text = text_to_binary(text)
encode_phase('input_audio.wav', binary_text)
decoded_binary = decode_phase('encrypted_audio.wav')
decoded_text = binary_to_text(decoded_binary)
print("Decrypted Text:", decoded_text)
