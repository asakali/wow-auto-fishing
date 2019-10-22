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
	
def find_match(img_rgb, prefix, max, threshold = 0.85):
	#print('Looking for float {}'.format(time.time()))
	# todo: maybe make some universal float without background?  

	images_path = os.path.join(get_work_dir(), 'images')

	for x in range(0, max):
		target_path = os.path.join(images_path, prefix + '_' + str(x) + '.png')

		template = cv2.imread(target_path, 0)	
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		
		w, h = template.shape[::-1]
		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
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

def find_drawing(threshold):
	return find_match(screen_cap.screen_left(), 'drawing', 0 + 1, threshold)

def find_lastpage():
	return find_match(screen_cap.screen_img_np(), 'lastpage', 0 + 1)
	
def find_nextpage():
	return find_match(screen_cap.screen_img_np(), 'nextpage', 0 + 1)
	
def find_money(threshold):
	return find_match(screen_cap.screen_left(), 'money', 0 + 1, threshold)
	
def find_npc():
	return find_match(screen_cap.screen_img_np(), 'npc', 0 + 1)

def find_lianjin_formula(threshold):
	return find_match(screen_cap.screen_left(), 'lianjin', 2 + 1, threshold)

def find_role_select_button():
	return find_match(screen_cap.screen_img_np(), 'role_select_button', 0 + 1)

def find_role():
	return find_match(screen_cap.screen_img_np(), 'role', 0 + 1)

def jump():
	probability = random.uniform(0.03, 0.05)
	
	while random.random() < probability:
		pyautogui.press(' ')
		time.sleep(random.uniform(1.2, 1.5))

def do_move(key, hold_time):
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.press(key)

def move_on():
	probability = random.uniform(0.03, 0.05)
	
	while random.random() < probability:
		do_move("w", probability)
		do_move("s", probability)
		do_move("a", probability)
		do_move("d", probability)
		time.sleep(random.uniform(1.2, 1.5))

def move_mouse_to_center():
	area = screen_cap.window_area()
	pyautogui.moveTo(int(area[2] / 2), int(area[3] / 2) + random.randint(10, 20), random.uniform(0.1, 0.5))

def move_mouse_rand():
	area = screen_cap.window_area()
	pyautogui.moveTo(random.randint(area[0], area[2]), random.randint(area[1], area[3]), random.uniform(0.15, 0.25))
	
def change_account():
	while True:
		place = find_role_select_button()

		if place:
			pyautogui.moveTo(place[0], place[1], random.uniform(0.1, 0.5))
			pyautogui.click(button = 'left')
			time.sleep(random.uniform(25, 30))

			place = find_role()

			if place:
				pyautogui.moveTo(place[0], place[1], random.uniform(0.1, 0.5))
				pyautogui.click(button = 'left', clicks = 2)
				time.sleep(random.uniform(15, 25))
				
				#pyautogui.hotkey('shift', 'tab')
				
				move_mouse_to_center()
				pyautogui.click(button = 'left')
				break
		else:
			time.sleep(random.uniform(1, 1.5))
			pyautogui.press('esc')
			time.sleep(random.uniform(1, 1.5))