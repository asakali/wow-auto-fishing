import random
import util
import pyautogui

loop_ts = 0
skills = ["1", "4", "3", "t"]

def working(now):
	global loop_ts

	if now - loop_ts > random.uniform(2.5, 5):
		s = random.choice(skills)
		pyautogui.press(s)

		if random.random() < random.uniform(0, 0.1):
			util.move_mouse_rand()
		
		if random.random() < random.uniform(0, 0.1):
			pyautogui.press(' ')

		# pyautogui.mouseDown(button='right')
		# pyautogui.mouseUp(button='right')

		loop_ts = now