# -*- coding: utf-8 -*-
import webbrowser
import sys
import os
import struct
import time
#
from win10toast import ToastNotifier
from threading import Thread
from infi.systray import SysTrayIcon

from datetime import datetime
from win32gui import GetWindowText, GetForegroundWindow

import random
import screen_cap, fishing_op, buy_op, unlock_op, jump_op, util
import datetime
import argparse

if __name__ == "__main__":
	util.set_work_dir()
	
	parser = argparse.ArgumentParser()
	parser.add_argument("action", help="given action", type = str)
	parser.add_argument('--throw', action='store_true', help='whether throw rubbish(default: no)')
	parser.add_argument('-c', dest = 'color', default='red', help='Float color support(red | orange | yellow | black)(default: red)')

	args = parser.parse_args()

	print("------ Auto throw rubbish {} ------".format("Enable" if args.throw else "Disable"))
	print("------ Float Color {} ------".format(args.color))

	while True:
		now = time.time()
		
		if GetWindowText(GetForegroundWindow()) == "魔兽世界":
			if args.action == "fishing":
				fishing_op.working(now, args.throw, args.color)

			if args.action == "buy":
				buy_op.working(now)

			if args.action == "unlock":
				unlock_op.working(now)

			if args.action == "jump":
				jump_op.working(now)
				
		# if cv2.waitKey(1) == 27:
		# 	break