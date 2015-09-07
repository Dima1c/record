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
from sys import (stdout)
from signal import (SIGTERM)
from docopt import (docopt)
from subprocess import (Popen, PIPE)

from Raw.Raw import (Raw)

VERSION = "record.py 1.0.0"

def crprint(msg):
    print '\r%s\r%s\r' % (' '*79, msg),
    stdout.flush()

def prompt(pre, s, post):
    crprint('%s: "%s".  --Press any key to %s.--' % (pre, s, post))
    with Raw() as raw:
        while not raw.kbhit(): pass
        raw.getch()
    crprint('')

def keep(source):
    target = ''
    for c in source:
        if c.isalnum() or c in ['_', '-']:
            target += c
        elif c == ' ':
            target += '.'
    return target

def record(phrase, **kw):
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
        pass

if __name__ == "__main__":

    def test():
        phrases = ["hello world", "klatu barada nikto", "fubar" ]
        print 'The following recordings are less than 2 minutes of speech.'
        for phrase in phrases:
            record(phrase)

    def main(**kw):
        if kw.get('--unit', False):
            test()
        else:
            for phrase in kw.get('<phrase>', []):
                record(phrase)

    kwargs = docopt(__doc__, version=VERSION)

    main(**kwargs)
