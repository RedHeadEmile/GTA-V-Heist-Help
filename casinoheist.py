import cv2
import numpy as np
from PIL import Image, ImageGrab
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
				moves.append("Q") # go left
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
		keyboard.press_and_release(key)
		sleep(0.025)

	print("Broke in ", datetime.now() - start, "\n---------------------")

	digit_hack_started = False


def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale


circles = [[(480, 320, 480 + 40, 320 + 40), (585, 320, 585 + 40, 320 + 40), (690, 320, 690 + 40, 320 + 40), (795, 320, 795 + 40, 320 + 40), (910, 320, 910 + 40, 320 + 40), (1015, 320, 1015 + 40, 320 + 40)],
[(480, 425, 480 + 40, 425 + 40), (585, 425, 585 + 40, 425 + 40), (690, 425, 690 + 40, 425 + 40), (795, 425, 795 + 40, 425 + 40), (910, 425, 910 + 40, 425 + 40), (1015, 425, 1015 + 40, 425 + 40)],
[(480, 540, 480 + 40, 540 + 40), (585, 540, 585 + 40, 540 + 40), (690, 540, 690 + 40, 540 + 40), (795, 540, 795 + 40, 540 + 40), (910, 540, 910 + 40, 540 + 40), (1015, 540, 1015 + 40, 540 + 40)],
[(480, 640, 480 + 40, 640 + 40), (585, 640, 585 + 40, 640 + 40), (690, 640, 690 + 40, 640 + 40), (795, 640, 795 + 40, 640 + 40), (910, 640, 910 + 40, 640 + 40), (1015, 640, 1015 + 40, 640 + 40)],
[(480, 750, 480 + 40, 750 + 40), (585, 750, 585 + 40, 750 + 40), (690, 750, 690 + 40, 750 + 40), (795, 750, 795 + 40, 750 + 40), (910, 750, 910 + 40, 750 + 40), (1015, 750, 1015 + 40, 750 + 40)]]

hacking_machine_started = False
def hacking_machine():

	global hacking_machine_started
	if hacking_machine_started:
		return

	hacking_machine_started = True

	img = ImageGrab.grab(bbox)

	txt = "----------------\n"
	for line in circles:
		txt += "  "
		for circle in line:
			txt += "o " if calculate_brightness(img.crop(circle)) > 0.3 else "- "
		txt += "\n"
	txt += "----------------"

	print(txt if txt.count("o") == 6 else "Nothing detected")

	hacking_machine_started = False
