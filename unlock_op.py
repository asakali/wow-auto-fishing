import pyautogui, random

loop_ts = 0

def working(now):
	global loop_ts

	if now - loop_ts > random.uniform(15, 20):
		pyautogui.click(button = 'right')

		loop_ts = now