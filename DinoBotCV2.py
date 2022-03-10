import numpy as np
import cv2
from mss import mss
from PIL import Image
import keyboard
import threading
import queue
import math

Val = cv2.imread("DinoHead",cv2.IMREAD_UNCHANGED)
Val1 = cv2.imread("Cactus1",cv2.IMREAD_UNCHANGED)
Val2 = cv2.imread("Cactus2",cv2.IMREAD_UNCHANGED)

my_queue1 = queue.Queue()
my_queue2 = queue.Queue()
sct = mss()
bounding_box = {"top": 0, "left": 0, "width": 950, "height": 800}
"""
def FindeGreenColor():
		# FIND THE GREEN COLOR
		sct_img = sct.grab(bounding_box)

		img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
		hsv = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2HSV)
	
		l_green = np.array([35,70,70])
		u_green = np.array([100, 255, 255])
		
		mask = cv2.inRange(np.array(hsv),l_green,u_green)
		output = cv2.bitwise_and(np.array(hsv), np.array(hsv), mask = mask)
		
		cv2.imshow("winn",output)
			
		#-----------------------------------
"""
def findCac1(max_loc_D,img,sct_img):
		#sct_img = sct.grab(bounding_box)
		#img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
		hsv = cv2.cvtColor(np.array(sct_img),cv2.COLOR_RGB2HSV)
	
		l_green = np.array([35,70,70])
		u_green = np.array([100, 255, 255])
		
		mask = cv2.inRange(np.array(hsv),l_green,u_green)
		output = cv2.bitwise_and(np.array(hsv), np.array(hsv), mask = mask)
			
		matchHSV = cv2.matchTemplate(np.array(output)[:,:],np.array(Val1)[:,:],cv2.TM_CCOEFF)
			
		min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(matchHSV)
		D_x,D_y = max_loc_D
		x,y = max_loc
		
		dx = D_x - x
		dy = D_y - y
		
		dis = math.sqrt(dx*dx+dy*dy)
		
		if dis < 100:
			print("jump")
			print(dis)
			keyboard.press_and_release('space')


def findCac2(max_loc_D,img,sct_img):
		#sct_img = sct.grab(bounding_box)
		#img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
		hsv = cv2.cvtColor(np.array(sct_img),cv2.COLOR_RGB2HSV)
		
		l_green = np.array([35,70,70])
		u_green = np.array([100, 255, 255])
					
		mask = cv2.inRange(np.array(hsv),l_green,u_green)
		output = cv2.bitwise_and(np.array(hsv), np.array(hsv), mask = mask)
					
		matchHSV = cv2.matchTemplate(np.array(output)[:,:],np.array(Val2)[:,:],cv2.TM_CCOEFF)
					
		min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(matchHSV)
		
		D_x,D_y = max_loc_D
		x,y = max_loc
		
		dx = D_x - x
		dy = D_y - y
		
		dis = math.sqrt(dx*dx+dy*dy)
		
		if dis < 100:
			print("jump")
			print(dis)
			keyboard.press_and_release('space')


def mainloop():
		while True:
			sct_img = sct.grab(bounding_box)
			img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
			
			
			match = cv2.matchTemplate(np.array(img)[:,:,:],np.array(Val)[:,:,:],cv2.TM_CCOEFF)
			
			min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(match)

			threashold = 0.5
			if max_val >=threashold:
				#Dino_w = Val.shape[1]
				#Dino_h = Val.shape[0]
				

				#top_l = max_loc
				#bottom_r = (top_l[0]+Dino_w,top_l[1]+Dino_h)

				#sct_img = cv2.rectangle(np.array(sct_img),top_l,bottom_r,(0,255,0),2)
				t3 = threading.Thread(target=findCac1,args=(max_loc,img,sct_img,))
				t3.start()
				t2 = threading.Thread(target=findCac2,args=(max_loc,img,sct_img,))
				t2.start()
				cv2.imshow("windows1",np.array(sct_img))
			if (cv2.waitKey(1) & 0xFF)==ord('c'):
				cv2.destroyAllWindows()
				break;


t1 = threading.Thread(target=mainloop)
t1.start()
