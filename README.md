# remorse
remorse plays randomly generated morse code for you to copy by pen and
paper.

You can control alphabet, speed, length, etc, run remorse --help for
details.

You may want to pipe stderr to /dev/null when running it - alsa and
friends generate a lot of warning messages that can usually be ignored.

For example:

remorse -a "krmso" 2> /dev/null

will play strings of morse code using the letters k, r, m, s and o. Once
it has finished playing, remorse will print the string and then exit.
