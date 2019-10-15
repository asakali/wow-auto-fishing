import pyautogui, random, time
import screen_cap, util

def jump():
	while random.random() < 0.2:
		pyautogui.press(' ')
		time.sleep(random.uniform(1.1, 3.5))

def cast():
	jump()
	pyautogui.press('`')

def move_mouse_to(x, y):
	pyautogui.moveTo(x, y, random.uniform(0.15, 0.35))

def snatch(x, y):
	move_mouse_to(x, y)

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

	pyautogui.press('esc')
	times = random.randrange(1, 7, 2)

	while times > 0:
		time.sleep(random.uniform(0.3, 1))
		pyautogui.press('esc')
		times -= 1
		
	time.sleep(random.uniform(1.5, 2))