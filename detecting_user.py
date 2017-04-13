import cv2
import sys
import httplib, urllib, base64
import json
import os
from time import sleep
import re
import time

wordlist = []
start_time=time.time()
elapsed_time=time.time()-start_time


cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
frequency=0
video_capture = cv2.VideoCapture(0)
i=0
count=0
blhh=0
k=0
z=0


def conversation():
	os.system("say 'you look beautiful today, do you mind if i take a picture today and tweet it to your handle?'")
	#reply = speech.answer()
	reply = 'no'
	sleep(1)
	if 'no' in reply :
		os.system("say ' do you want to know about upcoming events schedule here'")
		#reply= speech.answer()
	if 'yes' or 'sure' or 'why not' in reply:
		os.system("say 'Please give me a good pose'")
		#click_pic()
		#success = tweet()
		success = False
		if success == True:
			os.system("say 'I have tweeted pic to your handle, thank you'")
			os.system("say 'do you want to know about upcoming events schedule here'")
			
		else:
			os.system("say 'sorry, i am facing some network issues'")
			os.system("say 'do you want to know about upcoming events schedule here in the meanwhile'")
			
					



def add_face(person_id):
   headers = {
	   # Request headers
	   'Content-Type': 'application/octet-stream',
	   'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }


   body1={}
   body1['personGroupId']='1210'
   body1['personId']=person_id
   body1_d=json.dumps(body1)
   params = urllib.urlencode(body1)
   body=""
   f = open(img_file, "rb")
   body = f.read()
   f.close()

   try:
	   conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	   conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % params,body,headers)
	   response = conn.getresponse()
	   data = response.read()
	   print(data)
	   print "Your face has been added to your person Id"
	   conn.close()
   except Exception as e:
	   print("[Errno {0}] {1}".format(e.errno, e.strerror))




def add_person(name):
  headers = {
	  # Request headers
	  'Content-Type': 'application/json',
	  'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
  }

  params = urllib.urlencode({
	'personGroupId':'1210'
  })
  body = {}
  body["name"]= name
  body_d=json.dumps(body)


  conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
  conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons?%s" % params, body_d, headers)
  response = conn.getresponse()
  data = response.read()
  person_id=json.loads(data)
  person__id=person_id['personId']
  print "please note down your Unique person ID while i am training myself"
  print(person__id)
  database = open('/users/parasmanisharma/desktop/database.txt','a')
  database.write(data + " " + name+"\n") 
  database.close()

  conn.close()
  add_face(person__id)





def train_group(): 
   headers = {
	# Request headers
	'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }

   params = urllib.urlencode({
   'personGroupId':'1210'
   })

   try:
	   conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	   conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/train?%s" % params, "{}", headers)
	   response = conn.getresponse()
	   data = response.read()
	   print(data)
	   print "Training complete"
	   conn.close()
   except Exception as e:
	   print("[Errno {0}] {1}".format(e.errno, e.strerror))






def face_detection():
   k='0'
   headers = {
		# Request headers
	   'Content-Type': 'application/octet-stream',
	   'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }

   params = urllib.urlencode({
	   # Request parameters
	   'returnFaceId': 'true',
	   'returnFaceLandmarks': 'false'
   })

   body=""
   f = open(img_file, "rb")
   body = f.read()
   f.close()

   conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
   conn.request("POST", "/face/v1.0/detect?%s" % params,body, headers)
   response = conn.getresponse()
   data = response.read()

   #checking if any face is detected
   if data=="[]": 
	  j=2000
   else:
	  kim = json.loads(data)
	  l= kim[0]['faceId']   #faceId received
	  print l
	  k =json.dumps(l)



###############################################################################
	  #sending faceId to server for identification
   
   headers = {
	   # Request headers
	   'Content-Type': 'application/json',
	   'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }


   params = urllib.urlencode({
   })


   conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
   conn.request("POST", "/face/v1.0/identify?%s" % params, '{"personGroupId":"1210","faceIds":['+k+']}',headers)

	#personId recieved
   response = conn.getresponse()
   data = response.read()
   try:
	  data_json=json.loads(data)
	  l=data_json[0]['candidates'][0]['personId']
	  print data
	  database = open('/users/parasmanisharma/desktop/database.txt','r')
	  for line in database:
		  wordlist =line.split()
		  for words in wordlist:
			 if words == l:
				print "hello kitty"
				print  "hello "+wordlist[1]
				cmd = "say hello "+wordlist[1]
				os.system(cmd)
	  database.close() 
   except IndexError:
	   print "exception applied" 
   except KeyError:
	   print "lll"
   #conversation()



   try :
	  if data_json['error']['code'] == 'FaceNotFound': 
		  j=2000
   except TypeError:
	   print "exception 1 successfully applied"
   try: 
	  candidate=data_json[0]['candidates']
	  #if new face, ask for name
	  if candidate==[] :
		  #start_conversation("new_person")
		  os.system(" say ' You look new, please enter your name' ")
		  name = raw_input("You look new, please enter your name: ")
		  add_person(name)
		  train_group()
   except KeyError:
	   print "exception 2 successfullt applied" 


   print(data)     
   sleep(2)
   conn.close()



#additional_algorithm_by: github.com/prssharma77

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
	if (time.time()-start_time > 14 and k==7):


	   os.system("say 'User left, resetting program' ")
	   start_time=time.time()
	   k=9
	   print "in one"
	   frequency=0
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		if (time.time() - start_time <4 and k!=9):
			start_time = time.time()
			print start_time
			print "in two"
   
		else:

			k=7
			if frequency ==0:
			   start_time=time.time()
			   print "in threee"
			print "in four"
			os.system("say 'user detected in frame'")
			x=faces.size
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			frequency = frequency +1
			print frequency
			blhh=blhh+1
			sleep(1)

			cv2.imwrite("frame%d.jpg" % count, frame)     # save frame as JPEG file
			img_file= "frame%d.jpg" % count
			print "file saved %s" % img_file
			print "calling face detection"
			#lap_time =time.time()
			face_detection()
			#lap_time=time.time()-lap_time
			#start_time=start_time+lap_time
			print "start time = %f" % start_time
			blhh=0
		
	
