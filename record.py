#!/usr/bin/env python

"""\
record.py
Copyright(c) 2015 Jonathan D. Lettvin, All Rights Reserved.
License: GPLv3 http://www.gnu.org/licenses/gpl-3.0.en.html

Use record.py to acquire short sound samples in the style of a tape recorder.

For each phrase, a prompt is given to acquaint the speaker with the phrase.
After hitting a key, recording begins and continues until hittins another key.
The sample is recorded in a file.

Usage:
    record.py <phrase> [<phrase>...]
    record.py (-h | --help)
    record.py (-u | --unit)
    record.py --version

Options:
    -u, --unit  Run the unit tests.  [default: False]

A file named "phrase.<phrase>.wav" is generated for each phrase given.
For instance, if 'record.py "hello world"' is run, a file named
phrase.hello.world.wav is generated.
"""

from os import (kill)
from sys import (stdout, exc_info)
from signal import (SIGTERM)
from docopt import (docopt)
from subprocess import (Popen, PIPE)

from Raw.Raw import (Raw)

VERSION = "record.py 1.0.0"


def crprint(msg):
    "crprint outputs a same-line msg."
    print '\r%s\r%s\r' % (' '*79, msg),
    stdout.flush()


def prompt(pre, msg, post):
    "prompt shows a message, listens for a raw key, then clears the message."
    crprint('%s: "%s".  --Press any key to %s.--' % (pre, msg, post))
    with Raw() as raw:
        while not raw.kbhit():
            pass
        raw.getch()
    crprint('')


def keep(source):
    "keep converts a phrase to filename characters."
    target = ''
    for char in source:
        if char.isalnum() or char in ['_', '-']:
            target += char
        elif char == ' ':
            target += '.'
    return target


def record(phrase, **kw):
    "record uses prompts and sox to collect a sound sample."
    prefix, ext = [kw.get('prefix', 'phrase'), kw.get('ext', 'wav')]
    filename = '%s.%s.%s' % (prefix, keep(phrase), ext)
    options = ['-c 2', '-r 16000 -b 16 -c 1']
    command = 'rec -q %s %s trim 0 2:00' % (options[1], filename)
    try:
        prompt('Preparing', phrase, 'start')
        pid = Popen(command.split(), stderr=PIPE).pid
        prompt('Recording', phrase, 'stop')
        kill(pid, SIGTERM)
    except:
        print 'Unexpected exception:', exc_info()[0]

if __name__ == "__main__":

    def test():
        "test is a simple unit-test."
        phrases = ["hello world", "klatu barada nikto", "fubar"]
        print 'The following recordings are less than 2 minutes of speech.'
        for phrase in phrases:
            record(phrase)

    def main(**kw):
        "The starting point of execution."
        if kw.get('--unit', False):
            test()
        else:
            for phrase in kw.get('<phrase>', []):
                record(phrase)

    KWARGS = docopt(__doc__, version=VERSION)

    main(**KWARGS)
