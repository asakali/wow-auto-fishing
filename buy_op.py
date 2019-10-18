import pyautogui, random, time
import screen_cap, util
from PIL import Image
import pytesseract

lasttime = 0

pytesseract.pytesseract.tesseract_cmd = r'E:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "E:\\Program Files\\Tesseract-OCR\\tessdata"'

def buy_fuwenbubao():
	count = 3
	
	while count > 0:
		place = util.find_drawing()
		
		if place:
			place = util.find_money()
			
			if place:
				pyautogui.moveTo(place[0] - 70, place[1] - 30, random.uniform(0.01, 0.05))
				pyautogui.click(button = 'right', clicks = 3, interval = random.uniform(0.1, 0.2))

				# image = screen_cap.screen_rectangle(place[0], place[1] - 280, place[0] + 350, place[1])
				# text = pytesseract.image_to_string(Image.fromarray(image), lang='chi_sim', config = tessdata_dir_config)
				# print(text)
				
				time.sleep(random.uniform(1, 5))

		time.sleep(random.uniform(0.01, 0.05))
		count -= 1

		if not next_page():
			return

def find_npc():
	util.move_mouse_to_center()

	#open trade dialog
	pyautogui.click(button = 'right', clicks = 3, interval = random.uniform(0.1, 0.2))

	buy_fuwenbubao()
	pyautogui.press('esc')

	util.jump()
	
def last_page():
	place = util.find_lastpage()
	
	if place:
		pyautogui.moveTo(place[0], place[1], random.uniform(0.05, 0.1))
		pyautogui.click(button = 'left')
		pyautogui.moveTo(place[0] + random.randint(100, 200), place[1] + random.randint(100, 200), random.uniform(0.05, 0.1))

def next_page():
	place = util.find_nextpage()
	
	if place:
		pyautogui.moveTo(place[0], place[1], random.uniform(0.05, 0.1))
		pyautogui.click(button = 'left')
		pyautogui.moveTo(place[0] + random.randint(100, 200), place[1] + random.randint(100, 200), random.uniform(0.05, 0.1))
		
		return True

	return False

def working(now):
	global lasttime
	
	if now - lasttime > random.uniform(1, 1.5):
		find_npc()
		lasttime = now