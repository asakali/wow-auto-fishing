import pyautogui, random, time
import screen_cap, util
from PIL import Image
import pytesseract

loop_ts = 0
change_account_ts = time.time()

pytesseract.pytesseract.tesseract_cmd = r'E:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "E:\\Program Files\\Tesseract-OCR\\tessdata"'

def buy_npc_1():
	count = 3
	nextpage_place = util.find_nextpage()
	
	if nextpage_place:
		pyautogui.moveTo(nextpage_place[0], nextpage_place[1], random.uniform(0.01, 0.03))
		
		while count > 0:
			place = util.find_drawing(0.87)
			
			if place:
				print("found drawing")
				place = util.find_money(0.92)
				
				if place:
					print("found money")
					pyautogui.moveTo(place[0] - 70, place[1] - 30, random.uniform(0.01, 0.05))
					pyautogui.click(button = 'right', clicks = 3, interval = random.uniform(0.1, 0.2))
					
					break
					# image = screen_cap.screen_rectangle(place[0], place[1] - 280, place[0] + 350, place[1])
					# text = pytesseract.image_to_string(Image.fromarray(image), lang='chi_sim', config = tessdata_dir_config)
					# print(text)

			pyautogui.click(button = 'left')
			count -= 1

#炼金术供应商
#购买炼金图纸
def buy_lianjin():
	pyautogui.press('`')
	time.sleep(random.uniform(0.5, 0.6))
	place = util.find_lianjin_formula(0.88)
	is_success = False

	if place:
		print("found npc_0 selling")
		
		pyautogui.moveTo(place[0] - random.randint(75, 85), place[1], random.uniform(0.01, 0.05))
		pyautogui.click(button = 'right', clicks = 3, interval = random.uniform(0, 0.1))

		is_success = True

	end_buy_op()

	return is_success

def find_npc_1():
	# if random.random() < 0.1:
	# 	util.move_mouse_to_center()
	# 	pyautogui.click(button = 'left', clicks = 3, interval = random.uniform(0.1, 0.2))

	pyautogui.press('`')
	time.sleep(random.uniform(0.5, 0.6))

	buy_npc_1()
	end_buy_op()

def end_buy_op():
	time.sleep(random.uniform(0.2, 0.3))
	pyautogui.press('esc')
	util.move_mouse_rand()
	util.jump()
	time.sleep(random.uniform(0.2, 0.3))

def last_page():
	place = util.find_lastpage()
	
	if place:
		pyautogui.moveTo(place[0], place[1], random.uniform(0.01, 0.03))
		pyautogui.click(button = 'left')
		pyautogui.moveTo(place[0] + random.randint(100, 200), place[1] + random.randint(100, 200), random.uniform(0.01, 0.03))

def next_page():
	place = util.find_nextpage()
	
	if place:
		pyautogui.moveTo(place[0], place[1], random.uniform(0.01, 0.03))
		pyautogui.click(button = 'left')
		pyautogui.moveTo(place[0] + random.randint(100, 200), place[1] + random.randint(100, 200), random.uniform(0.01, 0.03))
		
		return True
		
	return False

def working(now):
	global loop_ts
	global change_account_ts

	if now - loop_ts > random.uniform(0.6, 1):
		if buy_lianjin():
			util.change_account()
			change_account_ts = now
			
		if now - change_account_ts > 18 * 60:
			util.change_account()
			change_account_ts = now
			
		loop_ts = now