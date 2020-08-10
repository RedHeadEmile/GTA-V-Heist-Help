import cv2
import numpy as np
from PIL import Image, ImageGrab
from threading import Thread
import pynput
import keyboard # need this lib instead of pynput for input because GTAV don't work with
from time import sleep
from datetime import datetime # optional, just for console printing

bbox = (0, 0, 1920, 1080) # for the screenshot

tofind = (950, 155, 1335, 685) # big digit box

# parts of digits to check
parts = [[(482, 279, 482 + 102, 279 + 102), (0, 0)],
[(627, 279, 627 + 102, 279 + 102), (1, 0)],
[(482, 423, 482 + 102, 423 + 102), (0, 1)],
[(627, 423, 627 + 102, 423 + 102), (1, 1)],
[(482, 566, 482 + 102, 566 + 102), (0, 2)],
[(627, 566, 627 + 102, 566 + 102), (1, 2)],
[(482, 711, 482 + 102, 711 + 102), (0, 3)],
[(627, 711, 627 + 102, 711 + 102), (1, 3)]]


def is_in(img, subimg):
	"""return if 'subimg' is in 'img'"""
	subimg1 = cv2.cvtColor(np.array(subimg), cv2.COLOR_BGR2GRAY) # need gray image to do the matchTemplate
	res = cv2.matchTemplate(img, subimg1, cv2.TM_CCOEFF_NORMED)
	threshold = 0.65 # error coef
	loc = np.where(res >= threshold)
	for pt in zip(*loc[::-1]):
		return True
	return False


digit_hack_started = False # used to prevent the function to be executed multiple times at once
def digit_hack():
	"""All the process to do the 'hack'"""
	start = datetime.now()

	global digit_hack_started
	if digit_hack_started: # prevent multiple runnings
		return

	digit_hack_started = True
	
	im = ImageGrab.grab(bbox) # take a screnshot

	sub0_ = im.crop(tofind); # cutting the image
	sub0 = cv2.cvtColor(np.array(sub0_.resize((round(sub0_.size[0] * 0.77), round(sub0_.size[1] * 0.77)))), cv2.COLOR_BGR2GRAY) # need to resize the image because fingerprints parts is smaller than the image + need gray image to do the matchTemplate

	# will store the location of the rights fingerprints
	togo = [part[1] for part in parts if is_in(sub0, im.crop(part[0]))]

	# closing every images
	sub0_.close()
	im.close()

	moves = [] # will store the moves to do

	x, y = 0, 0
	for pos in togo:
		while x != pos[0]:
			if x > pos[0]:
				x -= 1
				moves.append("q") # go left
			else:
				x += 1
				moves.append("d") # go right
		
		while y != pos[1]:
			if y > pos[1]:
				y -= 1
				moves.append("z") # go up
			else:
				y += 1
				moves.append("s") # go down
		moves.append("return") # select the fingerprints after being at the right place
	moves.append("tab") # validate the selection

	print("Calculate in ", datetime.now() - start)

	# execute every moves
	print(moves)
	for key in moves:
		break
		keyboard.press_and_release(key)
		sleep(0.025)

	print("Broke in ", datetime.now() - start, "\n---------------------")

	digit_hack_started = False


pressed = []
def on_press(key):
	"""Function used by pynput for it listener"""
	if key in pressed:
		return True
	pressed.append(key)

	try:
		k = key.char
	except:
		k = key.name

	if k == "f7":
		return False

	elif k == "f5":
		thread = Thread(target = digit_hack)
		thread.start() # run it async so can kill the process anyway with F7


def on_release(key):
	"""Function used by pynput for it listener"""
	if key in pressed:
		pressed.remove(key)


listener = pynput.keyboard.Listener(on_press = on_press, on_release = on_release)
listener.start()
listener.join()