# Breakout
Matt Williams' repository for Breakout
Co-developed by James Cunningham (james.cunningham.18@cnu.edu)

## Getting started
Firstly, Python 3.7 is needed for this. If not already installed, [it can be installed here](https://www.python.org/downloads/release/python-377/). Make sure to choose the option in the installer to include it in the PATH.

To download the game files, click the button labelled "Clone or download", and choose "Download ZIP". Once downloaded, extract the files from the File Explorer to the desired location. Then, navigate into the "breakout-master" subdirectory containing Breakout.py using the command line ([a tutorial on navigating the command line](https://www.computerhope.com/issues/chusedos.htm)). Once in the folder containing the file "Breakout.py", enter the following command into the command prompt:

`python Breakout.py`

This should start the game!


##Playing the game
The goal of Breakout is the break all the bricks without allowing your ball to fall off the bottom of the screen. In this version, the player has three lives, with one being depleated for each time the ball falls off-screen. Once all lives are depleated, the game is over. Each time the ball hits a brick, the score increases by one. When all bricks on the screen are destroyed, the next level begins, containing more bricks than the last level. Additionally, the new bricks will have more health (requiring more hits before being destroyed). In its current state, the game only has three unique levels; once level three is beaten, the third level restarts. The game can be played indefinitely, either until all lives are depleated or until the player exits the game.

###Controls
Move paddle: left/right arrow keys
Start game: Enter
Pause/unpause: Space
Exit game: Escape
