import cv2
import numpy as np
import screen_cap
import time

def find_match(img_rgb, prefix, max):
	#print('Looking for float {}'.format(time.time()))
	# todo: maybe make some universal float without background?  
	for x in range(0, max):   
		template = cv2.imread('images/' + prefix + '_' + str(x) + '.png', 0)	
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

		w, h = template.shape[::-1]
		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
		threshold = 0.8
		loc = np.where( res >= threshold)

		for pt in zip(*loc[::-1]):
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

		if loc[0].any():
			if False:
				print('Found ' + str(x) + ' ' + prefix)
				cv2.imwrite('images/session_' + prefix + str(int(time.time())) + '_success.png', img_rgb)

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