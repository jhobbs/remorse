import math
from pyaudio import PyAudio

BITRATE = 16000

def sine(frequency, length):
    wave_data = ''
    number_of_frames = int(BITRATE * length)
    for x in xrange(number_of_frames):
        wave_data += chr(int(math.sin(x/((BITRATE/frequency)/math.pi))*127+128))
    return wave_data


def silence(length):
    wave_data = ''
    number_of_frames = int(BITRATE * length)
    for x in xrange(number_of_frames):
        wave_data += chr(128)
    return wave_data


def play(wave_data):
    framecount = len(wave_data)
    restframes = framecount % BITRATE
    for x in xrange(restframes):
        wave_data += chr(128)

    chunk_size = BITRATE/10
    chunks = (len(wave_data) / chunk_size)

    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)

    for x in range(chunks):
        start = x * chunk_size
        finish = start + chunk_size
        stream.write(wave_data[start:finish])

    stream.stop_stream()
    stream.close()
    p.terminate()
