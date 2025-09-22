import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import queue, threading, collections

# Audio settings
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
WINDOW_SIZE = SAMPLE_RATE * 2

# Thread-safe queue for audio chunks
q = queue.Queue()

#buffer
buffer = collections.deque(maxlen=WINDOW_SIZE)

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata[:, 0].copy())  # Mono

# Start audio stream in a background thread
stream = sd.InputStream(
    channels=1,
    samplerate=SAMPLE_RATE,
    blocksize=CHUNK_SIZE,
    callback=audio_callback
)
stream.start()

# Set up matplotlib figure
plt.ion()
fig, ax_wave = plt.subplots(1, 1, figsize=(10, 6))

x_wave = np.arange(WINDOW_SIZE) / SAMPLE_RATE
line_wave, = ax_wave.plot(x_wave, np.zeros(WINDOW_SIZE))
ax_wave.set_ylim(-1, 1)
ax_wave.set_xlim(0, WINDOW_SIZE / SAMPLE_RATE)
ax_wave.set_title("Live Audio Waveform")
ax_wave.set_xlabel("Time (s)")
ax_wave.set_ylabel("Amplitude")


try:
    while True:
        chunk = q.get()
        buffer.extend(chunk)

        # Update waveform
        if len(buffer) == WINDOW_SIZE:
            line_wave.set_ydata(buffer)


        plt.pause(0.001)  # Allow UI refresh
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop()
    stream.close()
