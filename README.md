# Blackbox

This is a logic based game programed in Python.

All files are required for play, and you need to run Blackbox_full.py to initiate the game.

The history and rules of the game can be found:
https://en.wikipedia.org/wiki/Black_Box_(game)

It can be played as a single player game (select 1-5 atoms) or as a 2 player game where the 2nd player
selects the location of the atoms.  

The "main" player of the game then "shoots rays" into the center "black box" of the game and based on 
the output (or no output) can deduce where the atoms are within the black box.

Black colored markers signify a hit.  I.e. The ray the player shot from that location directly intersected
an atom within the board during its travels.

White colored markers signify a reflection.  The ray the player shot has an atom directly to the left or right
of it as it entered the board.

All other colored markers signify the entry and exit points of the rays shot.

You can guess the location of an atom at any time.  If you guess correctly, a green marker will show in the square.  
If you guess incorrectly, a red marker shows up in the square.

Players start with 25 points and one point is deducted for each entry or exit location on the board of a ray and 
5 points deducted for each wrong atom guess.

The game is over when the player has run out of points(lost) or guessed all of the atoms(won).

I am continuing to expand this game's overall organization to follow more closely "clean coding" guidelines of 
splitting out the functions to do "one thing" as well as make my code more readable without the need for as many
comments.  

Happy playing!
John
