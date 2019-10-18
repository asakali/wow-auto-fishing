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
import screen_cap, fishing_op, buy_op, util
import datetime

debug = True

if __name__ == "__main__":
	util.set_work_dir()
	
	while True:
		now = time.time()
		
		if GetWindowText(GetForegroundWindow()) == "魔兽世界":
			#fishing_op.working(now)
			buy_op.working(now)
			
		if cv2.waitKey(1) == 27:
			break