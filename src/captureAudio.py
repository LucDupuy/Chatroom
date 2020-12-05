import pyaudio
import wave
import sounddevice as sd
import numpy as np


SAMPLES = 1024
BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
SAMPLE_FREQ = 44100
SECONDS = 5
FILENAME = "output.wav"


def main():
    p = pyaudio.PyAudio()

    print("Recording")

    stream = p.open(format=BIT_DEPTH,
                    channels=CHANNELS,
                    rate=SAMPLE_FREQ,
                    frames_per_buffer=SAMPLES,
                    input=True
                    )

    # Byte array to store audio
    arr = []

    # Store 5 seconds
    for i in range(0, int(SAMPLE_FREQ / SAMPLES * SECONDS)):
        data = stream.read(SAMPLES)
        arr.append(data)

    # Close stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Finished Recording")
    play_stream(arr)
    #save(arr)


def play_stream(data_array):
    sd.play(data_array, SAMPLE_FREQ)

def save(data_array):
    # Save as WAV
    file = wave.open(FILENAME, 'wb')
    file.setnchannels(CHANNELS)
    file.setsampwidth(p.get_sample_size(BIT_DEPTH))
    file.setframerate(SAMPLE_FREQ)
    file.writeframes(b''.join(data_array))
    file.close()


if __name__ == '__main__':
    main()