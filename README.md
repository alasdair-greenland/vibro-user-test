# vibro-user-test
User test for a system that allows users to send/received emoticons via trackpad/vibrations

## Key for inputs:
Hitting f will full screen the page.
Hitting q will exit the page and print out the results.

# Version 1: Swipe Series
swipe-down = angry 😡
swipe-up = cry 😥
swipe-left = yay 😊
swipe-right = haha 😆
double-click = like 👍
right-click = heart ❤️
new-line = long click

# Version 2: Click Series
double-top-left = haha 😆
double-top-right = yay 😊
double-bottom-left = cry 😥
double-bottom-right = angry 😡
right-click-top = like 👍
right-click-bottom = heart ❤️

How do different vibration patterns and touch-based input methods affect users’ accuracy, speed, and confidence when sending and receiving emoticon messages without visual or auditory cues?

- H₁: Distinct rhythmic vibration patterns (varying in duration + pauses) will yield higher recognition accuracy and faster response times than patterns differing only in intensity.

- H₂: Spatial click-based gestures on the trackpad (e.g., quadrant double-clicks) will be more accurate and faster to perform eyes-free than directional swipe-based gestures, because the spatial layout provides a stronger mental map of emoji positions.

# Method:
Each participant will complete all four combinations:
(Rhythm + Swipe)
(Rhythm + Click)
(Intensity + Swipe)
(Intensity + Click)

# Procedure
Training Phase:
- Before each condition, participants learn the current vibration encoding and input mapping through guided practice (≈2–3 minutes).
- The learning process will consist of them listening to a video and following its instructions to ensure they learn it properly. 
- They train until they can confidently identify and send each emoticon.

# Testing Phase:
- Each trial begins with a vibration pattern representing an emoticon.
- Participants respond using the assigned input method (swipe or quadrant click).
- The system records response time and accuracy.
- Each block includes one randomized presentation of all six emoticons (repeated twice).

# Breaks & Transitions:
- A short rest (≈1 minute) separates each block. (maybe survey after each block)
- After blocks they transition to the next method of input/output

# Post-Study Survey:
- After completing all blocks, participants rate perceived difficulty, confidence, and preference for each combination (1–5 Likert scales).

- Tell participates how many trials
- tell tehm two sets of 6, insruct them to pinch the vibration motor falt.
- Counter balance the order jhave three do one three do the other
- Add repetition
- Analysingf the data, when we get data how do we anaylys mistacts with machine learninhg and the classifying, correct rate lable, incorrect label, miidle is good, difference between which confusion happened, angey? What was the common mistake, track common mistacks, make confusion matrics.

Phase one: mastery test

# Data Formatting
For the vibration sensing:
Files are named p(n)-t(n)-s(n).csv, with the ns meaning the participant number, trial number, and set used, respectively. The first column in the csv file is the actual symbol sent was, and the second column is what the user thought the symbol was.

For the inputting:
Files are named p(n)-input-s(n).csv, with the ns meaning the participant number and set used, respectively. The formatting is the same: the first column is the symbol the user was meant to input (pattern was the same every time), and the second column is what they actually inputted. Sometimes there was no input or the program didn't pick up the input; there are marked by leaving the second column blank.