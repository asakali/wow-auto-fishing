import cv2
import numpy as np
import screen_cap
import time
import os, sys
import pyautogui, random

work_dir = ""

def set_work_dir():
	global work_dir
	
	if hasattr(sys, "frozen"):# synchronize with pyloader's initialization.py
		#work_dir = os.path.abspath(os.path.join(os.path.dirname(os.__file__),'..'))
		work_dir = os.path.abspath(os.path.join(os.path.dirname(os.__file__)))
	else:
		work_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

def get_work_dir():
	global work_dir
	return work_dir
	
def find_match(img_rgb, prefix, max):
	#print('Looking for float {}'.format(time.time()))
	# todo: maybe make some universal float without background?  

	images_path = os.path.join(get_work_dir(), 'images')

	for x in range(0, max):
		target_path = os.path.join(images_path, prefix + '_' + str(x) + '.png')

		template = cv2.imread(target_path, 0)	
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		
		w, h = template.shape[::-1]
		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
		threshold = 0.9
		loc = np.where( res >= threshold)

		for pt in zip(*loc[::-1]):
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

		if loc[0].any():
			if False:
				print('Found ' + str(x) + ' ' + prefix)
				cv2.imwrite(images_path + '/session_' + prefix + str(int(time.time())) + '_success.png', img_rgb)

			return (loc[1][0] + w / 2), (loc[0][0] + h / 2)

	return None
	
def find_float():
	return find_match(screen_cap.screen_img_np(), 'float', 6 + 1)

def find_loud():
	return find_match(screen_cap.screen_img_np(), 'loud', 10 + 1)

def find_feather():
	return find_match(screen_cap.screen_img_np(), 'feather', 2 + 1)

def find_shell():
	return find_match(screen_cap.screen_img_np(), 'shell', 0 + 1)

def find_rod():
	return find_match(screen_cap.screen_img_np(), 'rod', 0 + 1)

def find_bait():
	return find_match(screen_cap.screen_img_np(), 'bait', 0 + 1)

def find_drawing():
	return find_match(screen_cap.screen_img_np(), 'drawing', 0 + 1)

def find_lastpage():
	return find_match(screen_cap.screen_img_np(), 'lastpage', 0 + 1)

def find_nextpage():
	return find_match(screen_cap.screen_img_np(), 'nextpage', 0 + 1)

def find_money():
	return find_match(screen_cap.screen_img_np(), 'money', 1 + 1)

def find_npc():
	return find_match(screen_cap.screen_img_np(), 'npc', 0 + 1)

def jump():
	probability = random.uniform(0.01, 0.015)
	
	while random.random() < probability:
		pyautogui.press(' ')
		time.sleep(random.uniform(0.05, 0.5))

	time.sleep(random.uniform(0.5, 1))

def move_mouse_to_center():
	area = screen_cap.window_area()
	pyautogui.moveTo(int(area[2] / 2), int(area[3] / 2) + 50, random.uniform(0.1, 0.5))