import random
import util
import pyautogui
import time

loop_ts = 0
skills = [("7"), ("2"), ("T"), ("T"), ("T"), ("T"),
	("shift", "1"), ("shift", "1"), ("shift", "1"), ("shift", "1"), 
	("shift", "5"), 
	("alt", "5")]

def working(now):
	global loop_ts

	if now - loop_ts > random.uniform(2.5, 4):
		pyautogui.press('tab')
		s = random.choice(skills)

		if len(s) > 1:
			pyautogui.hotkey(s[0], s[1])
		else:
			pyautogui.press(s[0])

		if random.random() < random.uniform(0, 0.1):
			util.move_mouse_rand()
		elif random.random() < random.uniform(0, 0.1):
			pyautogui.press(' ')
		elif random.random() < random.uniform(0, 0.3):
			util.move_mouse_to_center_up()
			i = 0
			
			while i < 3:
				pyautogui.mouseDown(button='right')
				pyautogui.mouseUp(button='right')
				i = i + 1
				
				time.sleep(random.uniform(0.2, 0.5))

		loop_ts = now