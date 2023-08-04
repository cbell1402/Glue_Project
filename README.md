# Glue_Project
Project to track viscosity of glue after mixing

This project is a GUI to track the pressure as a function of time for the drying of glue.

## How to use
1. Download `main.py` and rename if you would like.
2. Ensure you have all the imported packages by downloading them according to your OS.
3. Run `main.py` (or whatever you renamed it to).
4. Click the Start button to beging tracking.

## Features
- Tracks pressure over four hours from the time the user presses the Start button.
- If, for some reason, the program crashes the data should still be available upon restart. It will repopulate itself and continue as normal until four hours have passed.
- If the program reopens within four hours the displayed pressure value will round to the nearest value ending in .0 or .5.
- Updates every 0.2 seconds to reduce resource usage.
- Disables Start button if a marker is present.

## There are four important buttons

Start - Simply adds a marker (orange) to the plot and begins tracker pressure in the box above the button.

Clear - Deletes the data associated with the marker, closes, and reopens the application. 

Exit - Your exit (X) button. When you close the application the marker data is saved and is available again as long as you are within four hours of initially pressing the start button. 

Press To Continue - Appears in the middle of the window when four hours have passed to prompt the user to mix a new batch of glue. Acts similar to the Clear button.

![image](https://github.com/cbell1402/Glue_Project/assets/93935192/955c2633-0930-4f00-a808-85552a1ce789)
