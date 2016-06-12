import itertools
import math
from pyaudio import PyAudio

BITRATE = 16000
FADE_LENGTH = 0.002
FADE_FRAMES = int(BITRATE * FADE_LENGTH)


def sine(frequency, length):
    """Generate a sine wave in 8-bit unsigned PCM format.

    Uses linear fading at the beginning and end to avoid click noise.

    Good reference on how simple digital sound generation works:
    http://www.cs.nmsu.edu/~rth/cs/computermusic/Simple%20sound%20generation.html

    We use s_n = (v * sin(2*pi*f*n/sr)) + 128 where:
    - n is the sample number.
    - s_n is sample n.
    - f is frequency in hertz.
    - sr is the sample rate in samples per second.
    - v is the volume in the range of 0 to 127.

    Adding 128 serves to center the samples at 128, which is silence in 8-bit
    unsigned PCM format.
    """
    wave_data = ''
    number_of_frames = int(BITRATE * length)
    factor = (float(frequency) * (math.pi * 2)) / BITRATE
    for n in xrange(number_of_frames):
        if n < FADE_FRAMES:
            volume_factor = float(n) / FADE_FRAMES
        elif number_of_frames - n < FADE_FRAMES:
            volume_factor = float(number_of_frames - n) / FADE_FRAMES
        else:
            volume_factor = 1
        volume = 127 * volume_factor
        zero_centered = int(math.sin(n * factor) * volume)
        wave_data += chr(zero_centered + 128)
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
