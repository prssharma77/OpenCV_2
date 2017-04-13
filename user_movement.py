
import cv2
import sys
import time
import os
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
frequency=0
video_capture = cv2.VideoCapture(0)
i=0
count=0
blhh=0
k=0
z=0
start_time= time.time()
x1=0
#additional_algorithm_by: github.com/prssharma77
#wait for two seconds to enter the frame for first time and entering again after leaving

while True:

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)
    cv2.waitKey(10)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(40, 40),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if (time.time()-start_time > 4 and k==7):
       
       if x<400:
       	os.system("say 'User moved to the right side' ")
       elif x>600:
       	os.system("say 'User moved to the left side' ")
       else:
        os.system("say 'user left, resetting program'")
		
       start_time=time.time()
       k=9
       frequency=0
       print "in one"
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
    	z=faces.size
    	print z
    	if z!=x1:
    		cmd = "say " + 'i see %d people' % (z/4)
    		os.system(cmd)
    		x1=z
        if (time.time() - start_time <2 and k!=9):
            start_time = time.time()
            print "in two"
           
        else:
			
			k=7
			
			
			if frequency ==0:
			   start_time=time.time()
			   print "in three"
			os.system("say 'user detected in frame'")
			
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			print "in four"
		
			if z>0 :     #face detected by opencv
			   frequency = frequency +1
			   print z
			else :
			   print "error capturing image"
        
