#!/usr/bin/env python
import itertools
import sys
import audiogen

UNIT = 0.07 # Sounds close to 15 WPM.
DIT = UNIT
DAH = UNIT * 3


MORSE_CHARACTERS = {
    'a': (DIT, DAH,),
    'b': (DAH, DIT, DIT, DIT,),
    'c': (DAH, DIT, DAH, DIT,),
    'd': (DAH, DIT, DIT,),
    'e': (DIT,),
    'f': (DIT, DIT, DAH, DIT,),
    'g': (DAH, DAH, DIT,),
    'h': (DIT, DIT, DIT, DIT,),
    'i': (DIT, DIT,),
    'j': (DIT, DAH, DAH, DAH,),
    'k': (DAH, DIT, DAH,),
    'l': (DIT, DAH, DIT, DIT),
    'm': (DAH, DAH,),
    'n': (DAH, DIT,),
    'o': (DAH, DAH, DAH,),
    'p': (DIT, DAH, DAH, DIT,),
    'q': (DAH, DAH, DIT, DAH,),
    'r': (DIT, DAH, DIT,),
    's': (DIT, DIT, DIT,),
    't': (DAH,),
    'u': (DIT, DIT, DAH,),
    'v': (DIT, DIT, DIT, DAH,),
    'w': (DIT, DAH, DAH,),
    'x': (DAH, DIT, DIT, DAH,),
    'y': (DAH, DIT, DAH, DAH,),
    'z': (DAH, DAH, DIT, DIT,),
    '1': (DIT, DAH, DAH, DAH, DAH,),
    '2': (DIT, DIT, DAH, DAH, DAH,),
    '3': (DIT, DIT, DIT, DAH, DAH,),
    '4': (DIT, DIT, DIT, DIT, DAH,),
    '5': (DIT, DIT, DIT, DIT, DIT,),
    '6': (DAH, DIT, DIT, DIT, DIT,),
    '7': (DAH, DAH, DIT, DIT, DIT,),
    '8': (DAH, DAH, DAH, DIT, DIT,),
    '9': (DAH, DAH, DAH, DAH, DIT,),
    '0': (DAH, DAH, DAH, DAH, DAH,),
}


def timed_beep(frequency=440.0, seconds=0.25):
    for sample in audiogen.util.crop_with_fades(
            audiogen.tone(frequency), seconds=seconds):
        yield sample


def gen_character(character):
    for i, beat in enumerate(MORSE_CHARACTERS[character]):
        if i > 0:
            yield(audiogen.silence(UNIT))
        yield(timed_beep(seconds=beat))


def gen_string(input_string):
    for character in input_string:
        if character == ' ':
            yield audiogen.silence(UNIT * 6)
            continue
        for beat in gen_character(character):
            yield beat
        yield audiogen.silence(UNIT * 3)


audiogen.sampler.play(itertools.chain(*gen_string(sys.argv[1])))
