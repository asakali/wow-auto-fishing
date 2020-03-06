import random
import util
import pyautogui
import time

loop_ts = 0
skills = [("2"), ("3"), ("5"), ("7"), ("8"), ("0"), ("shift", "2")]

def working(now):
	global loop_ts

	if now - loop_ts > random.uniform(5, 10):
		pyautogui.press('tab')
		s = random.choice(skills)

		if len(s) > 1:
			pyautogui.hotkey(s[0], s[1])
		else:
			pyautogui.press(s[0])

			if s[0] == "7":
				time.sleep(random.uniform(15, 20))

		if random.random() < random.uniform(0, 0.1):
			util.move_mouse_rand()
		elif random.random() < random.uniform(0, 0.1):
			pyautogui.press(' ')

		loop_ts = now