import picamera
import picamera.array
import cv2
import numpy as np
import math

bgrLower = np.array([0, 100, 100]) 
bgrUpper = np.array([250,250, 250])

text = 'capture'
idx = 0



with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (640, 480)
        
        
        while True:
            
            idx += 1
            
            camera.capture(stream, 'bgr', use_video_port=True)
            camera.start_recording('/home/pi/Desktop/video.h264')
            stream.array = cv2.inRange(stream.array, bgrLower, bgrUpper)#Binalization
            
            ret, contours, hierarchy = cv2.findContours(stream.array, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )
            contours.sort(key=lambda x: cv2.contourArea(x), reverse=True)
            stream.array=cv2.drawContours(stream.array,contours[0:1],-1,(120,120,120),5)
            
            #Put lines in movies.
            x1=np.unravel_index(np.argmax(contours[0],axis=0), contours[0].shape)
            x2=np.unravel_index(np.argmax(contours[1],axis=0), contours[0].shape)
            stream.array = cv2.line(stream.array, tuple(x1[0][0]), tuple(x2[0][0]), (120,120,120), 3)
    
            #Subtitles
            if idx % 30 == 0:
                text =str(math.floor(np.linalg.norm(x1[0][0]-x2[0][0])))
            cv2.putText(stream.array, text,(0, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=3)


            cv2.imshow('frame', stream.array)
            
            

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            stream.seek(0)
            stream.truncate()
        cv2.destroyAllWindows()



