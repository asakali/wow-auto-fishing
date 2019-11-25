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

stat = {
	"do_bait": 0,
	"casting": 0,
	"catch": 0,
	"throw_rubbish": 0,
	"open_shell": 0
}

def cast():
	global stat

	util.jump()
	pyautogui.press('`')

	stat["casting"] = stat["casting"] + 1

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
	global stat
	exists = True
	
	pyautogui.press('b')
	time.sleep(random.uniform(1.5, 3))
	
	while exists:
		place = util.find_shell(0.8)

		if place:
			snatch(*place)
			time.sleep(random.uniform(1, 2))
			stat["open_shell"] = stat["open_shell"] + 1
		else:
			exists = False

	time.sleep(random.uniform(1.5, 3))
	pyautogui.press('b')
	
def throw_rubbish():
	global stat
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

			place_yes = util.find_button_yes(0.75)
			
			if place_yes:
				pyautogui.moveTo(place_yes[0], place_yes[1], random.uniform(0.1, 0.3))
				pyautogui.click(button='left')
				time.sleep(random.uniform(0.2, 0.4))

				stat["throw_rubbish"] = stat["throw_rubbish"] + 1
			else:
				print("not found button yes")
		else:
			print("not found rubbish")
			exists = False

		time.sleep(random.uniform(0.2, 0.4))

	time.sleep(random.uniform(1.5, 3))
	pyautogui.press('b')

def do_bait():
	global stat
	pyautogui.press('c')
	time.sleep(random.uniform(0.1, 0.3))

	pyautogui.press('b')
	time.sleep(random.uniform(0.5, 0.8))

	place = util.find_bait(0.8)

	if place:
		pyautogui.moveTo(place[0], place[1], random.uniform(0.1, 0.3))
		pyautogui.click(button='right')
		time.sleep(random.uniform(0.2, 0.4))
		
		place_rod = util.find_rod(0.8)
		
		if place_rod:
			pyautogui.moveTo(place_rod[0], place_rod[1], random.uniform(0.15, 0.4))
			pyautogui.click(button='left')
			time.sleep(random.uniform(6.5, 8))
			stat["do_bait"] = stat["do_bait"] + 1

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

def working(now, auto_throw, color):
	global is_block
	global begin_time
	global new_cast_time
	global frame_count
	global lastx
	global lasty
	global stat

	if is_block == False:
		lastx = 0
		lasty = 0
		frame_count = 0
		
		if now - begin_time > DO_BAIT_TIME:
			do_bait()
			open_clam_shell()
			
			if auto_throw:
				throw_rubbish()

			begin_time = now

			print("now:{} cast:{} catch:{} shell:{} throw:{} bait:{}".format(datetime.now(), 
																	stat["casting"], 
																	stat["catch"], 
																	stat["open_shell"], 
																	stat["throw_rubbish"], 
																	stat["do_bait"]))

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
		
		if color == 'black':
			#月光林地 60 53
			h_min = np.array((0, 0, 0), np.uint8)
			h_max = np.array((180, 255, 46), np.uint8)
		elif color == 'orange':
			#热砂岗  橙色
			h_min = np.array((11, 43, 46), np.uint8)
			h_max = np.array((25, 255, 255), np.uint8)
		elif color == 'yellow':
			h_min = np.array((26, 43, 46), np.uint8)
			h_max = np.array((34, 255, 255), np.uint8)
		else:
			#红色
			h_min = np.array((0, 43, 46), np.uint8)
			h_max = np.array((10, 255, 255), np.uint8)

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
				offset_x = 6
				offset_y = 6

				#在上方
				if lasty < ((area[3] - area[1]) / 2):
					offset_x = 5
					offset_y = 5

				if abs(b_x - lastx) > offset_x or abs(b_y - lasty) > offset_y:
					#print(abs(b_x - lastx), offset_x, abs(b_y - lasty), offset_y)
					snatch(area[0] + b_x, area[1] + b_y)
					move_mouse_to_free_area()
					is_block = False

					stat["catch"] = stat["catch"] + 1

			if frame_count % 4 == 0:
				lastx = b_x
				lasty = b_y

			frame_count += 1
		else:
			is_block = False

	if now - new_cast_time > RECAST_TIME:
		is_block = False