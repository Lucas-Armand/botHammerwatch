import cv2
import math
import numpy as np
import pyautogui as auto
from pynput import keyboard
from numpy import asarray
from threading import Thread

class botTask:
    def __init__(self):
        self._running = True
		self.x_pxl_center_screem = 1000
		self.y_pxl_center_screem = 550
		self.radius_click_around_character = 100

    def terminate(self):
        self._running = False

    def click(self,teta):
		# Method that control mouse to "click" a base attack in a specific angle (teta)
        cx = self.x_pxl_center_screem
        cy = self.y_pxl_center_screem
        r = self.radius_click_around_character
        a = math.sin(teta)
        b = math.cos(teta)
        auto.moveTo(cx+r*b,cy+r*a)
        auto.click()

    def find_nearest_white(self, img, target):
		# Method that recivies a image (img) and a target pixel (target) and return the nearest non zero pixel of the target 
        nonzero = cv2.findNonZero(img)
        distances = np.sqrt((nonzero[:,:,0] - target[0]) ** 2 + (nonzero[:,:,1] - target[1]) ** 2)
        nearest_index = np.argmin(distances)
        return nonzero[nearest_index]

    def angleBetweenTwoPixels(self,point1,point2):
		# Method that recivies two pixes and return the angle of the first (point1) relative to the second (point2)
		relative_point = point1 - point2 # Calculus of relative point
        teta = math.atan(relative_point[1]/relative_point[0])
        if relative_point[0]<1:
            teta = math.pi + teta
        return teta

    def findEnemiesOnMiniMap(self):
		# Method that scan in minimap red dots and return the angle of the closest enemy (or None if there isn't a enemy)  
        im = auto.screenshot(region=(1720,100,120,80))
        r, g, b = cv2.split(asarray(im))
        ret,thresh1 = cv2.threshold(r,200,255,cv2.THRESH_BINARY)

        # Erase hero simbol on minimap:
        thresh1[15:65,35:85] = np.zeros((50,50))
        cv2.findNonZero(thresh1)

        # If theres same Enemy near:
        if np.max(thresh1) == 255:

            # Find Closest Enemy
            point = self.find_nearest_white(thresh1,(40,60))
            point = point[0] 

            # Convert point to center's map relative angle
            teta = self.angleOfPoint(point,(60,40))

            return teta

        # If not return None
        return None


    def run(self, n):
        while self._running == True:
            teta = self.findEnemiesOnMiniMap()
            if teta:
                self.click(teta)


def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener

    if k == '9':  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        global b
        b = botTask()
        t = Thread(target = b.run, args =(10, ))
        t.start()

    if k == '0':  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        b.terminate()

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate threadli
    listener.join()
