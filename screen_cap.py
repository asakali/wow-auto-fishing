import cv2, imutils, numpy as np, PIL.ImageGrab as ImageGrab
from win32gui import GetForegroundWindow, GetWindowRect

def find_bobber(mask, output):
	''' Finds bobber based on contour detection within video feed.
		Recommended to use HSV or RGB mask.
		Returns the center point of the largest contour found.
			ARGS:		mask (cv2 HSV, RGB, or other filter)
						output (cv2 video output object)
			RETURNS:	center (tuple(X,Y)) or None
	'''
	center = None
	# Define contours
	cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	# No idea what this does
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	print(cnts)

	# If a contour is found
	if len(cnts) > 0:
		try:
		# Find the biggest contour
			c = max(cnts, key=cv2.contourArea)	
		# Get the position(x,y) and the radius
			((x,y), radius) = cv2.minEnclosingCircle(c)
		# Contour
			M = cv2.moments(c)
		# Find the center of the circle
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			# Show X,Y of circle on video feed
			cv2.putText(output,(str(f'Bobber Pos. (X,Y): ({int(x)},{int(y)})')),(10, (output.shape[0] - 10)),
								cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,255,255), 1)

			# Show X,Y of center
			cv2.putText(output,(str(f'Center: {center} Radius: {radius}')),(10, (output.shape[0] - 20)),
								cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,255,255), 1)

			# Draw the circle and center point
			cv2.circle(output, (int(x), int(y)), int(radius), (0,255,0), 2)
			cv2.circle(output, center, 5, (0,0,255), -1)
		except Exception as e:
			print("error occured")
			print(e)
			pass
	else:
		print('[-] Cant find bobber!')

	return center

def generate_window(x1, y1, x2, y2, lower_range=None, upper_range=None):
	''' Generates a recording window at the specified coordinates and applies
		an HSV mask to the captured video feed. If no lower_range or upper_range supplied,
		default values that worked for me will be used.
			ARGS:		x1,y1,x2,y2 (int)
			 (optional)	lower_range,upper_range (int list [H,S,V])
	'''
	screen = np.array(ImageGrab.grab(bbox=(x1,y1,x2,y2)))
	if lower_range and upper_range:
		pass
	else:
		# HSV Range that works for bobber for me
		lower_range = [38,0,0] # H, S, V
		upper_range = [255,255,255] # H, S, V
	# Apply filter to HSV video feed
	hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
	mask = hsv_mask(hsv, lower_range, upper_range)
	output = cv2.bitwise_and(hsv, hsv, mask=mask)
	return mask, output
	
def window_area():
	rect = GetWindowRect(GetForegroundWindow())
	area = (0, 0, rect[2], rect[3])
	
	return area
	
def valid_area():
	rect = GetWindowRect(GetForegroundWindow())
	fish_area = (rect[2] * 0.25, rect[3] * 0.25, rect[2] * 0.75, rect[3] * 0.75 - 100)
	
	return fish_area

def free_area():
	fish_area = valid_area()
	non_fish_area = (fish_area[0], 0, fish_area[2], fish_area[1])
	
	return non_fish_area

def screen_img_np():
	img = ImageGrab.grab(window_area())
	img_np = np.array(img)
	
	return img_np

def hsv_mask(hsv_image, lower_range, upper_range):
	''' Add HSV mask to the image. Returns HSV filtered image.
			ARGS: 		image (cv2 image object)
						lower_range, upper_range (list [H,S,V])
			RETURNS:	hsv_masked_image (cv2 image object)'''
	# Convert ranges to a numpy array
	lower_range = np.array(lower_range, dtype="uint8")
	upper_range = np.array(upper_range, dtype="uint8")
	return cv2.inRange(hsv_image, lower_range, upper_range)