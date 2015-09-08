#!/usr/bin/env python

"""\
PTT.py
Copyright(c) 2015 Jonathan D. Lettvin, All Rights Reserved.
License: GPLv3 http://www.gnu.org/licenses/gpl-3.0.en.html

Use PTT.py to acquire short sound samples in the style of a tape recorder.

For each phrase, a prompt is given to acquaint the speaker with the phrase.
After hitting a key, recording begins and continues until another key is hit.
The sample is recorded in a file.  This process repeats for each phrase.
Phrases are typically quoted strings.

Usage:
    PTT.py [-b <bits>] [-c <channels>] [-r <rate>] <phrase> [<phrase>...]
    PTT.py [-b <bits>] [-c <channels>] [-r <rate>] [-f <phrasefile>]
    PTT.py (-h | --help)
    PTT.py (-u | --unit)
    PTT.py --version

Options:
    -b, --bits=<bits>           Number of sample bits.      [default: 16]
    -c, --channels=<channels>   Mono=1, Stereo=2.           [default: 1]
    -f, --file=<phrasefile>     File containing phrases.    [default: None]
    -r, --rate=<rate>           Sampling rate.              [default: 16000]
    -u, --unit                  Run the unit tests.         [default: False]

A file named "phrase.<phrase>.wav" is generated for each phrase given.
For instance, if 'PTT.py "hello world"' is run, a file named
phrase.hello.world.wav is generated.

Some options are copied from the SoX command-line option list.
"""

from os import (kill)
from sys import (stdout, exc_info)
from signal import (SIGTERM)
from docopt import (docopt)
from subprocess import (Popen, PIPE)
from pprint import (pprint)
import pygame

VERSION = "PTT.py 1.0.0"


def crprint(msg):
    "crprint outputs a same-line msg."
    print '\r%s\r%s\r' % (' '*79, msg),
    stdout.flush()


def prompt(pre='Prompt', msg='Action required', post='continue'):
    "prompt shows a message, listens for a raw key, then clears the message."
    crprint('%s: "%s".  --Press any key to %s.--' % (pre, msg, post))
    char = ' '
    with Raw() as raw:
        while not raw.kbhit():
            pass
        char = raw.getch()
    crprint('')
    return char


def keep(source):
    "keep converts a phrase to filename characters."
    target = ''
    for char in source:
        if char.isalnum() or char in ['_', '-']:
            target += char
        elif char == ' ':
            target += '.'
    return target


def PTT(phrase, **kw):
    "PTT uses prompts and sox to collect a sound sample."
    prefix, ext = [kw.get('prefix', 'phrase'), kw.get('ext', 'wav')]
    filename = '%s.%s.%s' % (prefix, keep(phrase), ext)
    options = '-b %s -c %s -r %s' % (
            kw.get('--bits', 16),
            kw.get('--channels', 1),
            kw.get('--rate', 16000))
    rec = 'rec -q %s %s trim 0 2:00 +10' % (options, filename)
    play = 'play -q %s' % (filename)
    try:
        pid, recording, playing, confirm = 0, False, False, False
        print 'PTT <SPACE> "%s"\r' % (phrase),
        stdout.flush()
        collecting = True
        while collecting:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    recording = False
                    if pid:
                        kill(pid, SIGTERM)
                        pid = 0
                        playing = True
                        message = '<RETURN> "%s" to keep, %s to resample\r' % (
                                filename, '<SPACE>')
                        print message,
                        stdout.flush()
                elif event.type == pygame.KEYDOWN:
                    if not recording and event.key == pygame.K_SPACE:
                        recording = True
                        pid = Popen(rec.split(), stderr=PIPE).pid
                        print 'started "%s"     \r' % (phrase),
                        stdout.flush()
                    elif event.key == pygame.K_RETURN:
                        print filename, ' ' * 50
                        collecting = False
                        stdout.flush()
            if playing:
                Popen(play.split(), stderr=PIPE).pid
                playing = False
                confirm = True





            """
            prompt('Preparing', phrase, 'start')
            pid = Popen(rec.split(), stderr=PIPE).pid
            prompt('Recording', phrase, 'stop')
            kill(pid, SIGTERM)
            Popen(play.split(), stderr=PIPE).pid
            response = None
            while response == None:
                char = prompt('Sample collected', 'Keep? [Y/n]').upper()
                if char in ['Y', 'N']:
                    response = char
            if response == 'Y':
                break
            """
    except:
        pprint(exc_info())
        #print 'Unexpected exception:', exc_info()[0]

if __name__ == "__main__":

    def test():
        "test is a simple unit-test."
        phrases = ["hello world", "klatu barada nikto", "fubar"]
        print 'The following recordings are less than 2 minutes of speech.'
        for phrase in phrases:
            PTT(phrase)

    def main(**kw):
        "The starting point of execution."
        pygame.init()
        pygame.key.set_repeat(100, 100)
        if kw.get('--unit', False):
            test()
        else:
            phrasefile = eval(kw.get('--file', "None"))
            phrases = []
            if phrasefile:
                print '"%s"' % (phrasefile)
                with open(phrasefile) as source:
                    phrases = [line.strip() for line in source.readlines()]
            else:
                phrases = kw.get('<phrase>', [])
            if not phrases:
                print 'No phrases to record'
            else:
                for phrase in phrases:
                    PTT(phrase, **kw)

    KWARGS = docopt(__doc__, version=VERSION)

    main(**KWARGS)
