![logo](https://raw.githubusercontent.com/j4y-boi/pip-the-mouse/refs/heads/main/readme-assets/logov2Trimmed.png)
#  Your small mouse friend written in Python! (Made for Hackapet) 
Pip the Mouse is a small game/pet written for your Hackapet! You can watch him sleep, feed him, ... ~~If something goes wrong he'll start to climb walls so, watch out for that...~~  

# Wait what
You heard me right! Pip is built for the hackapet, dunno what that is? Go here -> [Hackapet](https://hackapet.hackclub.dev/)  
Pip was written using circuitPython, which is why he's named pip. Ya know, the python package installer, anyways.  

# Game Functions
- Feeding Pip an assortment of foods! (cheese, peanuts, apple slices, grapes)
- If he's bored he'll start to sleep
- Very important! If you feed him too much (or too little) he'll uhhh <sub>die</sub> ...
- He needs to exercise! Mice need activity too...
- Saving your game! So you can come back later to Pip.

# Game Controls
**PC:**
 - Left Arrow: Open Stats (Time before hunger/exercise, time alive)
 - Up Arrow: Open drop menu
 - Up + Left Arrow: Drop ball
 - Up + Right Arrow: Drop food
 - Right Arrow: Save game (There's also an autosave function that triggers every 30 seconds)
 - Left + Right Arrow: Delete save file (Restart game to confirm, right arrow to cancel)
  
**Hackapet:**
- I'll add support when I get one... (probably same as arrow keys tho)

# Playing it
Oh! You want to play the game! Sure, here are some instructions:
- Download the repo as a zip
- Optionally, if you feel like arraging stuff, make a virtual enviroment in Python using these commands:
```
python3 -m venv .env
source .env/bin/activate
```
- Next, install the necessary libraries using pip (see what I did there)
```
pip3 install blinka-displayio-pygamedisplay adafruit-circuitpython-display-text
```
- Now run main.py (while you're in your venv) and you should be good to go!

# Some screenshots
![a screenshot from one type of room (dark walls)](https://raw.githubusercontent.com/j4y-boi/pip-the-mouse/refs/heads/main/readme-assets/screenshots/screenshot1.png)
![a screenshot from one type of room (light walls)](https://raw.githubusercontent.com/j4y-boi/pip-the-mouse/refs/heads/main/readme-assets/screenshots/screenshot2.png)
![a screenshot from one type of room (blue walls)](https://raw.githubusercontent.com/j4y-boi/pip-the-mouse/refs/heads/main/readme-assets/screenshots/screenshot3.png)
![a screenshot of the stats menu (hunger)](https://raw.githubusercontent.com/j4y-boi/pip-the-mouse/refs/heads/main/readme-assets/screenshots/screenshot4.png)
![a screenshot of stats menu saying that Pip is hungry](https://raw.githubusercontent.com/j4y-boi/pip-the-mouse/refs/heads/main/readme-assets/screenshots/screenshot5.png)
![a screenshot of the dropdown menu](https://raw.githubusercontent.com/j4y-boi/pip-the-mouse/refs/heads/main/readme-assets/screenshots/screenshot6.png)
![a screenshot of pip being, uh dead?](https://raw.githubusercontent.com/j4y-boi/pip-the-mouse/refs/heads/main/readme-assets/screenshots/screenshot7.png)

# License
```
Pip the Mouse is licensed under the GPL-3.0 license,
a copy of which can be found in the LICENSE file in the repository. 
```
