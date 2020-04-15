import picamera
import picamera.array
import cv2
import numpy as np

bgrLower = np.array([0, 100, 100]) 
bgrUpper = np.array([250,250, 250])

text = 'capture'

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (640, 480)
        while True:
            
            camera.capture(stream, 'bgr', use_video_port=True)
            stream.array = cv2.inRange(stream.array, bgrLower, bgrUpper)
            cv2.putText(stream.array, text,(0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), thickness=2)
            cv2.imshow('frame', stream.array)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            stream.seek(0)
            stream.truncate()
        cv2.destroyAllWindows()


