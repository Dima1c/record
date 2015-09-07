#!/usr/bin/env python

"""\
record.py
Copyright(c) 2015 Jonathan D. Lettvin, All Rights Reserved.
License: GPLv3 http://www.gnu.org/licenses/gpl-3.0.en.html

record is used to acquire short sound samples in the style of a tape recorder.

Usage:
    record.py <sentence> [<sentence>...]
    record.py (-h | --help)
    record.py (-u | --unit)
    record.py --version

Options:
    -u, --unit  Run the unit tests.  [default: False]

A file named "sentence.<sentence>.wav" is generated for each sentence given.
For instance, if 'record.py "hello world"' is run, a file named
sentence.hello.world.wav is generated.
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

def record(sentence, **kw):
    prefix, ext = [kw.get('prefix', 'sentence'), kw.get('ext', 'wav')]
    filename = '%s.%s.%s' % (prefix, keep(sentence), ext)
    options = ['-c 2', '-r 16000 -b 16 -c 1']
    command = 'rec -q %s %s trim 0 2:00' % (options[1], filename)
    try:
        prompt('Preparing', sentence, 'start')
        pid = Popen(command.split(), stderr=PIPE).pid
        prompt('Recording', sentence, 'stop')
        kill(pid, SIGTERM)
    except:
        pass

if __name__ == "__main__":

    def test():
        sentences = ["hello world", "klatu barada nikto", "fubar" ]
        print 'The following recordings are less than 2 minutes of speech.'
        for sentence in sentences:
            record(sentence)

    def main(**kw):
        if kw.get('--unit', False):
            test()
        else:
            for sentence in kw.get('<sentence>', []):
                record(sentence)

    kwargs = docopt(__doc__, version=VERSION)

    main(**kwargs)
