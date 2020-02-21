import random
import util
import pyautogui

loop_ts = 0

skills = [("shift", "1"), 
	("shift", "3"), 
	("shift", "5"), 
	("shift", "6"), 
	("alt", "1"), 
	("alt", "2"),
	("alt", "3"), 
	("alt", "4")]

def working(now):
	global loop_ts

	if now - loop_ts > random.uniform(5, 15):
		if random.random() < random.uniform(0, 0.3):
			util.move_mouse_rand()
		elif random.random() < random.uniform(0, 0.3):
			s = random.choice(skills)
			pyautogui.hotkey(s[0], s[1])
		else:
			pyautogui.press(' ')

		loop_ts = now