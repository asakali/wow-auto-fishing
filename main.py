# -*- coding: utf-8 -*-
import webbrowser
import sys
import os
import struct
import time
#
import numpy as np
import cv2
#
from win10toast import ToastNotifier
from PIL import ImageGrab
from threading import Thread
from infi.systray import SysTrayIcon

from datetime import datetime
from win32gui import GetWindowText, GetForegroundWindow

import random
import screen_cap, fishing_op

debug = True
RECAST_TIME = 30
DO_BAIT_TIME = 10 * 60 + 10

if __name__ == "__main__":
	is_block = False
	begin_time = time.time()
	new_cast_time = 0
	frame_count = 0
	
	while True:
		now = time.time()

		if GetWindowText(GetForegroundWindow()) == "魔兽世界":
			fishing_op.do_bait()
			break
			if is_block == False:
				lastx = 0
				lasty = 0
				frame_count = 0
				
				if now - begin_time > DO_BAIT_TIME:
					fishing_op.do_bait()
					fishing_op.open_clam_shell()
					begin_time = now

				fishing_op.cast()
				
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

				h_min = np.array((11, 43, 46), np.uint8)
				h_max = np.array((34, 255, 255), np.uint8)

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
						if abs(b_x - lastx) > 4 or abs(b_y - lasty) > 4:
							fishing_op.snatch(area[0] + b_x, area[1] + b_y)
							fishing_op.move_mouse_to_free_area()
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

		if cv2.waitKey(1) == 27:
			break