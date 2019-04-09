import picamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import time

camera = picamera.PiCamera()
camera.resolution = (640 , 480)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size = (640,480) )
time.sleep(0.1)

upper_area = 30000
lower_area = 500

font = cv2.FONT_HERSHEY_COMPLEX
threshold = 0.15

templateShortcut1 = cv2.imread('aa.png',cv2.IMREAD_GRAYSCALE)
templateShortcut = cv2.Canny(templateShortcut1,75,150)
templateShortcutg1 = cv2.imread('slide1.png',cv2.IMREAD_GRAYSCALE)
templateShortcutg = cv2.Canny(templateShortcutg1,75,150)
templateShortcutr1 = cv2.imread('slide2.png',cv2.IMREAD_GRAYSCALE)
templateShortcutr = cv2.Canny(templateShortcutr1,75,150)
templateShortcutb1 = cv2.imread('slide3.png',cv2.IMREAD_GRAYSCALE)
templateShortcutb = cv2.Canny(templateShortcutb1,75,150)
templateShortcuty1 = cv2.imread('slide4.png',cv2.IMREAD_GRAYSCALE)
templateShortcuty = cv2.Canny(templateShortcuty1,75,150)
templateDistance1 = cv2.imread('Slide5.png',cv2.IMREAD_GRAYSCALE)
templateDistance = cv2.Canny(templateDistance1,75,150)
templateTLight1 = cv2.imread('Slide6.png',cv2.IMREAD_GRAYSCALE)
templateTLight = cv2.Canny(templateTLight1,75,150)
templateGoal1 = cv2.imread('Slide7.png',cv2.IMREAD_GRAYSCALE)
templateGoal = cv2.Canny(templateGoal1,75,150)
templateGoala1 = cv2.imread('Slide71.png',cv2.IMREAD_GRAYSCALE)
templateGoala = cv2.Canny(templateGoala1,75,150)
templateGoalb1 = cv2.imread('Slide72.png',cv2.IMREAD_GRAYSCALE)
templateGoalb = cv2.Canny(templateGoalb1,75,150)
templateRamp1 = cv2.imread('Slide8.png',cv2.IMREAD_GRAYSCALE)
templateRamp = cv2.Canny(templateRamp1,75,150)
templateShapes1 = cv2.imread('Slide9.png',cv2.IMREAD_GRAYSCALE)
templateShapes = cv2.Canny(templateShapes1,75,150)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   frame = frame.array
   gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
   dilate = cv2.Canny(gray,200,200)

   _,contours,_ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

   for cnt in contours:
      area = cv2.contourArea(cnt)
      approx = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
      x = approx.ravel()[0]
      y = approx.ravel()[1]
      if area > lower_area:
         cv2.drawContours(frame,[approx],0,(255,0,255),2)
         if len(approx) == 4:
                 cv2.putText(frame,"Quadrilateral",(x,y),font,0.5,(255,0,0))
                 pts1 = np.float32([approx[3],approx[0],approx[2],approx[1]])
                 pts2 = np.float32([[0,0],[320,0],[0,240],[320,240]])
                 matrix = cv2.getPerspectiveTransform(pts1,pts2)
                 result = cv2.warpPerspective(dilate,matrix,(320,240))
                 cv2.imshow("daw",result)
                 resShortcut = cv2.matchTemplate(result,templateShortcut,cv2.TM_CCOEFF_NORMED)
                 locShortcut = np.where(resShortcut >= threshold)
                 resShortcutg = cv2.matchTemplate(result,templateShortcutg,cv2.TM_CCOEFF_NORMED)
                 locShortcutg = np.where(resShortcutg >= threshold)
                 resShortcutr = cv2.matchTemplate(result,templateShortcutr,cv2.TM_CCOEFF_NORMED)
                 locShortcutr = np.where(resShortcutr >= threshold)
                 resShortcutb = cv2.matchTemplate(result,templateShortcutb,cv2.TM_CCOEFF_NORMED)
                 locShortcutb = np.where(resShortcutb >= threshold)
                 resShortcuty = cv2.matchTemplate(result,templateShortcuty,cv2.TM_CCOEFF_NORMED)
                 locShortcuty = np.where(resShortcuty >= threshold)
                 if len(locShortcut[1]>0) or len(locShortcutg[1]>0) or len(locShortcutr[1]>0) or len(locShortcutb[1]>0) or len(locShortcuty[1]>0):
                      #mask black
                      print("mask out black")
                 
                 resDistance = cv2.matchTemplate(result,templateDistance,cv2.TM_CCOEFF_NORMED)
                 locDistance = np.where(resDistance >= threshold)
                 if len(locDistance[1]>0):
                      #use ultrasonic
                      print("ultrasonic")
                 
                 resTLight = cv2.matchTemplate(result,templateTLight,cv2.TM_CCOEFF_NORMED)
                 locTLight = np.where(resTLight >= threshold)
                 if len(locTLight[1]>0):
                      #Stop until Traffic Light 
                      print("Traffic Light")
                      
                 resGoal = cv2.matchTemplate(result,templateGoal,cv2.TM_CCOEFF_NORMED)
                 locGoal = np.where(resGoal >= threshold)
                 resGoala = cv2.matchTemplate(result,templateGoala,cv2.TM_CCOEFF_NORMED)
                 locGoala = np.where(resGoala >= threshold)
                 resGoalb = cv2.matchTemplate(result,templateGoalb,cv2.TM_CCOEFF_NORMED)
                 locGoalb = np.where(resGoalb >= threshold)
                 if len(locGoal[1]>0) or len(locGoala[1]>0) or len(locGoalb[1]>0):
                      #Kick ball
                      print("ball")
                      
                 resRamp = cv2.matchTemplate(result,templateRamp,cv2.TM_CCOEFF_NORMED)
                 locRamp = np.where(resRamp >= threshold)
                 if len(locRamp[1]>0):
                      #MPU-6050
                      print("MPU")
                      
                 resShapes = cv2.matchTemplate(result,templateShapes,cv2.TM_CCOEFF_NORMED)                 
                 locShapes = np.where(resShapes >= threshold)         
                 if len(locShapes[1]>0):
                      #find shapes
                      print("Shapes")

#  cv2.imshow("video",frame)
#   cv2.imshow("mask",dilate)
#   rawCapture.truncate(0)
   key = cv2.waitKey(1) & 0xFF
   if key == ord("q"):
      break

#cv2.destroyAllWindows()
