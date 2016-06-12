import itertools
import math
from pyaudio import PyAudio

BITRATE = 16000
FADE_LENGTH = 0.002
FADE_FRAMES = int(BITRATE * FADE_LENGTH)


def sine(frequency, length):
    """Generate a sine wave for use with pyaudio.

    Uses linear fading at the beginning and end to avoid click noise.
    """
    wave_data = ''
    number_of_frames = int(BITRATE * length)
    factor = float(frequency) * (math.pi * 2) / BITRATE
    for x in xrange(number_of_frames):
        if x < FADE_FRAMES:
            volume_factor = float(x) / FADE_FRAMES
        elif number_of_frames - x < FADE_FRAMES:
            volume_factor = float(number_of_frames - x) / FADE_FRAMES
        else:
            volume_factor = 1
        volume = 127 * volume_factor
        wave_data += chr(int(math.sin(x * factor) * volume + 128))
    return wave_data


def silence(length):
    wave_data = ''
    number_of_frames = int(BITRATE * length)
    for x in xrange(number_of_frames):
        wave_data += chr(128)
    return wave_data


def play(wave_data):
    chunk_size = BITRATE/10

    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)

    for chunk in itertools.islice(wave_data, chunk_size):
        stream.write(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
