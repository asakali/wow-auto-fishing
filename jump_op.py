import random
import util

loop_ts = 0

def working(now):
	global loop_ts

	if now - loop_ts > random.uniform(3, 5):
		util.jump(0, 0.3)
		
		loop_ts = now