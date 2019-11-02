import pyautogui, random, time
import screen_cap, util
import numpy as np
import cv2
from PIL import ImageGrab
from datetime import datetime

pyautogui.FAILSAFE = False

RECAST_TIME = 30 + 2
DO_BAIT_TIME = 10 * 60 + 10

is_block = False
begin_time = time.time()
new_cast_time = 0
frame_count = 0
lastx = 0
lasty = 0

def cast():
	util.jump()
	pyautogui.press('`')

def move_mouse_to(x, y):
	pyautogui.moveTo(x, y, random.uniform(0.15, 0.35))

	pyautogui.FAILSAFE

def snatch(x, y):
	pyautogui.moveTo(x, y, random.uniform(0.08, 0.15))

	pyautogui.mouseDown(button='right')
	pyautogui.mouseUp(button='right')

def move_mouse_to_free_area():
	time.sleep(random.uniform(2.0, 3.3))
	free_area_rectangle = screen_cap.free_area()
	move_mouse_to(random.randint(free_area_rectangle[0], free_area_rectangle[2]), random.randint(free_area_rectangle[1], free_area_rectangle[3]))

def open_clam_shell():
	exists = True
	
	pyautogui.press('b')
	time.sleep(random.uniform(1.5, 3))
	
	while exists:
		place = util.find_shell()

		if place:
			snatch(*place)
			time.sleep(random.uniform(1, 2))
			print("open shell!!")
		else:
			exists = False

	time.sleep(random.uniform(1.5, 3))
	pyautogui.press('b')
	
def throw_rubbish():
	exists = True
	
	pyautogui.press('b')
	time.sleep(random.uniform(1.5, 3))
	
	while exists:
		place = util.find_rubbish()

		if place:
			pyautogui.moveTo(place[0], place[1], random.uniform(0.1, 0.3))
			pyautogui.click(button='left')
			time.sleep(random.uniform(0.2, 0.4))

			util.move_mouse_to_center()
			pyautogui.click(button='left')
			time.sleep(random.uniform(0.2, 0.4))

			place = util.find_button_yes(0.75)
			
			if place:
				pyautogui.moveTo(place[0], place[1], random.uniform(0.1, 0.3))
				pyautogui.click(button='left')
				time.sleep(random.uniform(0.2, 0.4))
			else:
				print("not found button yes")
		else:
			print("not found rubbish")
			exists = False

	time.sleep(random.uniform(1.5, 3))
	pyautogui.press('b')

def do_bait():
	pyautogui.press('c')
	time.sleep(random.uniform(0.1, 0.3))

	pyautogui.press('b')
	time.sleep(random.uniform(0.5, 0.8))

	place = util.find_bait()

	if place:
		pyautogui.moveTo(place[0], place[1], random.uniform(0.1, 0.3))
		pyautogui.click(button='right')
		time.sleep(random.uniform(0.2, 0.4))
		
		place = util.find_rod()
		
		if place:
			pyautogui.moveTo(place[0], place[1], random.uniform(0.15, 0.4))
			pyautogui.click(button='left')
			time.sleep(random.uniform(6.5, 8))

	pyautogui.press('c')
	time.sleep(random.uniform(0.1, 0.3))
	
	pyautogui.press('b')
	time.sleep(random.uniform(0.5, 0.8))
	
	# times = random.randrange(2, 6, 2)

	# while times > 0:
	# 	time.sleep(random.uniform(0.2, 0.5))
	# 	pyautogui.press('esc')
	# 	times -= 1

	# time.sleep(random.uniform(1.5, 2))

def working(now):
	global is_block
	global begin_time
	global new_cast_time
	global frame_count
	global lastx
	global lasty
	
	if is_block == False:
		lastx = 0
		lasty = 0
		frame_count = 0
		
		if now - begin_time > DO_BAIT_TIME:
			do_bait()
			open_clam_shell()
			throw_rubbish()
			begin_time = now
		
		cast()
		
		new_cast_time = now
		is_block = True
		
		#Here sleep at least 3 second for bobber disapper
		time.sleep(random.uniform(3, 4.5))
	else:
		area = screen_cap.valid_area()
		img = ImageGrab.grab(area)
		img_np = np.array(img)
		
		frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
		frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		if datetime.now().hour < 0:
			#辛特兰	热砂岗
			h_min = np.array((11, 43, 46), np.uint8)
			h_max = np.array((25, 255, 255), np.uint8)
		else:
			#月光林地 60 53
			h_min = np.array((0, 0, 0), np.uint8)
			h_max = np.array((180, 255, 46), np.uint8)

		#艾萨拉-破碎海岸 68 71
		#h_min = np.array((100, 43, 46), np.uint8)
		#h_max = np.array((124, 255, 255), np.uint8)
		
		mask = cv2.inRange(frame_hsv, h_min, h_max)
		
		# cv2.imshow('hsv',mask)
		# cv2.waitKey()
		# cv2.destroyAllWindows()

		moments = cv2.moments(mask, 1)
		dM01 = moments['m01']
		dM10 = moments['m10']
		dArea = moments['m00']

		if dArea > 0:
			b_x = int(dM10 / dArea)
			b_y = int(dM01 / dArea)

			if lastx > 0 and lasty > 0:
				offset_x = 5
				offset_y = 5

				if lasty < ((area[3] - area[1]) / 2):
					offset_x = 4
					offset_y = 4

				if abs(b_x - lastx) > offset_x or abs(b_y - lasty) > offset_y:
					snatch(area[0] + b_x, area[1] + b_y)
					move_mouse_to_free_area()
					is_block = False
					print("catch something!!")

			if frame_count % 4 == 0:
				lastx = b_x
				lasty = b_y

			frame_count += 1
		else:
			is_block = False

	if now - new_cast_time > RECAST_TIME:
		is_block = False