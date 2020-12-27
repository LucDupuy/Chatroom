import pyaudio
import wave
import sounddevice as sd
import numpy as np
import socket

print(socket.gethostbyname("ROGUEONE"))

SAMPLES = 1024
BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
SAMPLE_FREQ = 44100
SECONDS = 3
FILENAME = "output.wav"





def main():
    # rec_pyaudio()
   rec_sd()
   load()

def rec_pyaudio():
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

    # Stores recording
    for i in range(0, int(SAMPLE_FREQ / SAMPLES * SECONDS)):
        data = stream.read(SAMPLES)
        arr.append(data)

    # Close stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Finished Recording")
    play_stream(arr)
    # save(arr, p)


def rec_sd():
    recording = sd.rec(SECONDS*SAMPLE_FREQ, samplerate=SAMPLE_FREQ, channels=CHANNELS, dtype='float64')
    print("Recording")
    sd.wait()
    print("Finished Recording")
    print("Playing Recording")

    np.save('recording', recording)

   # sd.play(recording, SAMPLE_FREQ)
   # sd.wait()
   # print("Finished")



def play_stream(data_array):
    sd.play(data_array, SAMPLE_FREQ)

def save(data_array, p):
    # Save as WAV
    file = wave.open(FILENAME, 'wb')
    file.setnchannels(CHANNELS)
    file.setsampwidth(p.get_sample_size(BIT_DEPTH))
    file.setframerate(SAMPLE_FREQ)
    file.writeframes(b''.join(data_array))
    file.close()



def load():
    recording = np.load('recording.npy')
    print(recording)
    play_stream(recording)
    sd.wait()


if __name__ == '__main__':
    main()
