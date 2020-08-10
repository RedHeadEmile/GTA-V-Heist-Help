import cv2
import numpy as np
from PIL import Image, ImageGrab
from threading import Thread
import pynput
import keyboard # need this lib instead of pynput for input because GTAV don't work with
from time import sleep
from datetime import datetime # optional, just for console printing

tofind = (950, 155, 1335, 685) # big digit box

# parts of digits to check
dig1 = (482, 279, 482 + 102, 279 + 102)
dig2 = (627, 279, 627 + 102, 279 + 102)
dig3 = (482, 423, 482 + 102, 423 + 102)
dig4 = (627, 423, 627 + 102, 423 + 102)
dig5 = (482, 566, 482 + 102, 566 + 102)
dig6 = (627, 566, 627 + 102, 566 + 102)
dig7 = (482, 711, 482 + 102, 711 + 102)
dig8 = (627, 711, 627 + 102, 711 + 102)


def check(img, subimg, togo, identifier):
	"""If 'subimg' is in 'img', this function will add 'identifier' to the array 'togo'"""
	subimg1 = cv2.cvtColor(np.array(subimg), cv2.COLOR_BGR2GRAY) # need gray image to do the matchTemplate
	res = cv2.matchTemplate(img, subimg1, cv2.TM_CCOEFF_NORMED)
	threshold = 0.65 # error coef
	loc = np.where(res >= threshold)
	for pt in zip(*loc[::-1]):
		togo.append(identifier)
		return


bbox = (0, 0, 1920, 1080)
def screenshot():
	"""Take a screenshot and return a pil image"""
	return ImageGrab.grab(bbox)


digit_hack_started = False # used to prevent the function to be executed multiple times at once
def digit_hack():
	"""All the process to do the 'hack'"""
	start = datetime.now()

	global digit_hack_started
	if digit_hack_started: # prevent multiple runnings
		return

	digit_hack_started = True
	
	im = screenshot()

	sub0_ = im.crop(tofind); # cutting the image
	sub0_5 = sub0_.resize((round(sub0_.size[0] * 0.77), round(sub0_.size[1] * 0.77))) # need to resize the image because fingerprints parts is smaller than the image
	sub0 = cv2.cvtColor(np.array(sub0_5), cv2.COLOR_BGR2GRAY) # need gray image to do the matchTemplate

	# cutting the image
	sub1 = im.crop(dig1)
	sub2 = im.crop(dig2)
	sub3 = im.crop(dig3)
	sub4 = im.crop(dig4)
	sub5 = im.crop(dig5)
	sub6 = im.crop(dig6)
	sub7 = im.crop(dig7)
	sub8 = im.crop(dig8)

	togo = [] # will store the location of the rights fingerprints

	# checking every parts
	check(sub0, sub1, togo, (0, 0))
	check(sub0, sub2, togo, (1, 0))
	check(sub0, sub3, togo, (0, 1))
	check(sub0, sub4, togo, (1, 1))
	check(sub0, sub5, togo, (0, 2))
	check(sub0, sub6, togo, (1, 2))
	check(sub0, sub7, togo, (0, 3))
	check(sub0, sub8, togo, (1, 3))

	# closing every images
	sub0_.close()
	sub0_5.close()
	sub1.close()
	sub2.close()
	sub3.close()
	sub4.close()
	sub5.close()
	sub6.close()
	sub7.close()
	sub8.close()
	im.close()

	moves = [] # will store the moves to do

	x, y = 0, 0
	for i in range(len(togo)):
		i = togo[i]
		while x != i[0]:
			if x > i[0]:
				x -= 1
				moves.append("q") # go left
			else:
				x += 1
				moves.append("d") # go right
		
		while y != i[1]:
			if y > i[1]:
				y -= 1
				moves.append("z") # go up
			else:
				y += 1
				moves.append("s") # go down
		moves.append("return") # select the fingerprints after being at the right place
	moves.append("tab") # validate the selection

	print("Calculate in ", datetime.now() - start)

	# execute every moves
	for i in range(len(moves)):
		key = moves[i]
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