import cv2
import urllib.request
import numpy as np
from socket import gaierror
from datetime import datetime as dt
from gpiozero import MotionSensor
from multiprocessing import Process, Pipe
import mysql.connector
import subprocess
import json
import time as t
import logging

#This function includes the detection of the license plate. Credits to openalpr.
def detect_license_plate():    
    #subprocess module calls a linux terminal command and gets and output (see references 6, 7)
    print('detecting license...')
    start_time1 = t.time()
    process = subprocess.run(['alpr', '-c eu', '-p cz', '-n 3','-j',\
                              '/home/pi/projects/license-plate-detection/slanina/to_detect_from.jpg'],\
                             stdout=subprocess.PIPE, text=True)
    stop_time1 = t.time()
    dtt1 = stop_time1 - start_time1
    print(dtt1)
    #print(process.stdout,file=output_to_database)
    current_date = dt.now()   
    #takes output of subprocess and saves it
    diccionario = process.stdout
    #transforms subprocess output into json format (see reference 8)
    diccionario = json.loads(diccionario)
    #get result of the 'results' key
    #if empty, no plates detected        
    if diccionario['results']==[]:
        print('No plates detected')
    #if populated, print plate number and detection confidence
    elif diccionario['results']!=[]:
        #-----------------------------------------------------------------
        #for debugging purposes            
        print(diccionario['results'][0]['plate'])
        print(diccionario['results'][0]['confidence'])
        print(current_date)
        #-----------------------------------------------------------------
        plate = diccionario['results'][0]['plate']
        confidence = diccionario['results'][0]['confidence']
        #insert info into database
        connect_to_database = mysql.connector.connect(user='root', password='pi',
                                                      database='plates', host='localhost', port='3306')
        #-----------------------------------------------------------------
        #for debugging purposes
        #print(connect_to_database)
        #-----------------------------------------------------------------
        cursor = connect_to_database.cursor()
        #-----------------------------------------------------------------
        #for debugging purposes 
        #print(cursor)            
        #print(number)
        #-----------------------------------------------------------------
        #the format of the data for inserting it to database
        add_plate_info = ("INSERT INTO license_plates_detected "
          "(Plates, Confidence, Date) "
          "VALUES (%(Plates)s, %(Confidence)s, %(Date)s)")
        #-----------------------------------------------------------------
        #for debugging purposes
        #print(add_plate_info)
        #-----------------------------------------------------------------
        #the data to be inserted to database
        data_plate_info = {
            'Plates': plate,
            'Confidence': confidence,
            'Date': current_date,
            }
        #-----------------------------------------------------------------
        #for debugging purposes
        #print(data_plate_info)
        #-----------------------------------------------------------------
        #Insert the data
        cursor.execute(add_plate_info, data_plate_info)
        #Commit the insertion
        connect_to_database.commit()
        #Close cursor
        cursor.close()
        #close database
        connect_to_database.close() 

#function for PIR motion sensor: when it senses movement this makes a photo
def motion_sensor():    
    print('process 2 started')
    #signal when movement occurs coming from ping GPIO4 (see reference 5)
    pir = MotionSensor(4, threshold = 0.5)
    #pause the script until the sensor is activated, or timeout is reached (if specified)
#    motion = pir.motion_detected    
#    if motion == True:    
    pir.wait_for_motion()    
    #message for debugging purposes
    print("ha, I saw you.")
    #pause the script until the sensor is deactivated, or timeout is reached (if specified) 
    pir.wait_for_no_motion()    
    #call function for photo
    start_time = t.time()
    print("waiting child...")
    image1 = parent_conn.recv()
    cv2.imwrite('to_detect_from.jpg', image1)
    detect_license_plate()
    stop_time = t.time()
    dtt = stop_time - start_time
    print(dtt)
    
#    else:
#        pass
    #print(image)

def live_stream(conn):
    print('process 1 started')
    stream = urllib.request.urlopen('http://localhost:8081/', data=None)
    bytess = b''

    while(True):
        bytess += stream.read(1024)
        a = bytess.find(b'\xff\xd8')
#        print(a)
#        print('\n')
        b = bytess.find(b'\xff\xd9')
#        print(b)
#        print('\n')
        if a != -1 and b != -1:
            jpg = bytess[a:b+2]
            bytess=bytess[b+2:]
            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            conn.send(image)
            #print(image)
            cv2.imshow('image', image)
            if cv2.waitKey(1)==27:
                exit(0)


#live streaming from Motion, framerate 2 FPS
#------------------------------------------------------------------------
try:
    if __name__ == '__main__':
        parent_conn, child_conn = Pipe()
        p1 = Process(target=live_stream, args=(child_conn,))
        p2 = Process(target=motion_sensor)        
        
        p1.start() #start process 1
        p2.start() #start process 2
    
           
except OSError:    
    logging.basicConfig(filename='error_log.log', level = logging.DEBUG)
    exception_date = dt.now()
    logging.debug('Unable to get live feed. Verify the Motion project feed.'+ str(exception_date))
    raise

                
#------------------------------------------------------------------------
            
            
            
            
#References:
#1.https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
#2.https://picamera.readthedocs.io/en/release-1.13/recipes2.html
#3.http://doc.openalpr.com/accuracy_improvements.html
#4.https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
#5.https://gpiozero.readthedocs.io/_/downloads/en/stable/pdf/
#6.https://docs.python.org/3/library/subprocess.html
#7.https://www.youtube.com/watch?v=2Fp1N6dof0Y
#8.https://docs.python.org/3/library/json.html
#9.https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
#10.https://github.com/openalpr/openalpr/wiki/OpenALPR-Design
