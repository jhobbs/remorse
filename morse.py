#!/usr/bin/env python
import argparse
import itertools
import random
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


def play_character(character):
    for i, beat in enumerate(MORSE_CHARACTERS[character]):
        if i > 0:
            yield(audiogen.silence(UNIT))
        yield(timed_beep(seconds=beat))


def play_string(input_string):
    for character in input_string:
        if character == ' ':
            yield audiogen.silence(UNIT * 6)
            continue
        for beat in play_character(character):
            yield beat
        yield audiogen.silence(UNIT * 3)


def generate_random_string(alphabet, max_length, max_word_length):
    string_length = random.randint(1, max_length)

    word_length = 0
    for i in range(0, string_length):
        if word_length == max_word_length:
            if i == max_length - 1:
                return
            yield ' '
            word_length = 0
            continue

        if i > 0 and i < max_length - 1 and word_length > 0 and \
            random.randint(0, max_word_length) == 0:
            yield ' '
            word_length = 0
            continue

        yield random.choice(alphabet)
        word_length += 1


def get_random_string(alphabet, max_length, max_word_length):
    return ''.join(
        generate_random_string(alphabet, max_length, max_word_length))


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--max-word-length",
        help="Maximum word length. Default is 5.",
        default=5, type=int)
    parser.add_argument("-l", "--max-length",
        help="Maximum overall length. Default is 30.",
        default=30, type=int)
    parser.add_argument("-a", "--alphabet",
        help="Alphabet for words. Default is all letters and numbers.",
        default=MORSE_CHARACTERS.keys())
    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()
    message_string = get_random_string(
        alphabet=args.alphabet,
        max_length=args.max_length,
        max_word_length=args.max_word_length)
    play_list = play_string(message_string)
    samples = itertools.chain(*play_list)
    audiogen.sampler.play(samples)
    print(message_string)


if __name__ == '__main__':
    main()
