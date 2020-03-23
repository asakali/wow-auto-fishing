import random
import util
import pyautogui

loop_ts = 0
skills = [("shift", "1"), ("shift", "2"), ("shift", "1")]

def working(now):
	global loop_ts

	if now - loop_ts > random.uniform(10, 15):
		r = random.random()
		
		if r < 0.1:
			util.move_mouse_rand()
		elif r < 0.8:
			s = random.choice(skills)
			pyautogui.hotkey(s[0], s[1])
		else:
			pyautogui.press(' ')

		loop_ts = now