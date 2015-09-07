# record
Simple python sound recording CLI
---------------------------------

Using a pipe to spawn and kill a sox 'rec' instance,
this app enables the user to record short samples quickly and easily.
The premise is that the user has a number of phrases to record separately
and wishes to loop through the list, recording with a minimum of other action.

The challenges to achieve this were unusual.
After a fair amount of searching,
no cross-platform recording methods appeared to be
closer to the requirements than the SoX (Sound Exchange) app.

http://sox.sourceforge.net/

But even SoX doesn't have a simple start/stop capability.
This record.py app handles the requirement by spawning and killing.

    $ record.py "hello world" "He's dead, Jim." "Lucy.  I'm home."

will make three files in the current directory
after the user responds to the prompts:

    $ ls phrase.*.wav
    phrase.hello.world.wav  phrase.He.s.dead.Jim.wav  phrase.Lucy.I.m.home.wav

These files can be output using the SoX app 'play':

    $ play phrase.hello.world.wav

TODO:

This app is tested on MacOS Yosemite.
It may need work on Windows and linux.
