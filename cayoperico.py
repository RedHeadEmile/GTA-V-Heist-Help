import cv2
import numpy as np
from PIL import Image, ImageGrab
import keyboard # need this lib instead of pynput for input because GTAV don't work with
from time import sleep
from datetime import datetime # optional, just for console printing

bbox = (0, 0, 1920, 1080) # for the screenshot

targets = [(907, 331, 1562, 431), # split the big digit in 8 parts
(907, 404, 1562, 504),
(907, 500, 1562, 600),
(907, 560, 1562, 660),
(907, 627, 1562, 727),
(907, 697, 1562, 809),
(907, 780, 1562, 883),
(907, 863, 1562, 975)]

scan = [(424, 360, 810, 415), # every parts on the left
(424, 360 + 76, 810, 415 + 76),
(424, 360 + 76 * 2, 810, 415 + 76 * 2),
(424, 360 + 76 * 3, 810, 415 + 76 * 3),
(424, 360 + 76 * 4, 810, 415 + 76 * 4),
(424, 360 + 76 * 5, 810, 415 + 76 * 5),
(424, 360 + 76 * 6, 810, 415 + 76 * 6),
(424, 360 + 76 * 7, 810, 415 + 76 * 7)]


def index(part, parts):
	"""Return the index of 'part' in 'parts', return -1 if not found"""
	for i in range(len(parts)):
		res = cv2.matchTemplate(parts[i], part, cv2.TM_CCOEFF_NORMED)
		loc = np.where(res >= 0.65)
		for pt in zip(*loc[::-1]):
			return i
	return -1


digit_hack_started1 = False
def digit_hack():
	start = datetime.now()

	global digit_hack_started1
	if digit_hack_started1:
		return

	digit_hack_started1 = True

	im = ImageGrab.grab(bbox) # take the screenshot

	parts = []
	for target in targets:
		part = im.crop(target)
		# resite the big part and store it
		parts.append(cv2.cvtColor(np.array(part.resize((round(part.size[0] * 0.91), round(part.size[1] * 0.91)))), cv2.COLOR_BGR2GRAY))

	moves = []
	for i in range(len(scan)):
		# get the index of the litle part on  the left
		j = index(cv2.cvtColor(np.array(im.crop(scan[i])), cv2.COLOR_BGR2GRAY), parts)
		while j != i: # the index must be the same as 'i', then move to it so
			if j > i:
				moves.append("Q")
				j -= 1
			else:
				moves.append("D")
				j += 1

		moves.append("S")

	print(moves)
	for key in moves:
		keyboard.press_and_release(key)
		sleep(0.025)

	print("Broke in ", datetime.now() - start, "\n---------------------")

	digit_hack_started1 = False