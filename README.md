# GTAV fingerprints hack

* Did in `python`
* You need a `1920x1080` resolution, otherwise you will have to get the new positions of every fingerprints (little parts and the big one).
* You need the packages `opencv`, `numpy`, `Pillow`, `pynput` and `keyboard`


# How to use it ?
* Be in the fingerprints hack screen and be able to move
* Press F5
* Enjoy
* By pressing F7 you will close the program

# How it works ?
* The script take a screenshot
* Resize and cut it
* Compare the fingerprints parts with the big fingerprints
* Determine which keys to press

# Problems you could have
* Wrong keys: the script work with `zqsd` (azerty keyboard), to change it, open the script and change `zqsd` to `wasd` near line `70`