import json
import requests
import os
import time
import threading as thread 

# local
from connection import Connection
import mysqlConnector
from config import read_config
from checkTask import checking 


def callback_converter(ch, method, properties, body):
	"""function colled when the queue is not empty"""

	params = read_config(section = 'parameters')#get parameters config
	path_config = read_config(section='path')#get path confg
	jsonVideo = json.loads(body)
	print jsonVideo
	file_path = jsonVideo['file_path']
	fileName = getFileName(file_path)
	videoPath = path_config['videopath']#path to download video
	# response = requests.get(file_path)

	"""checked video"""
	videoId = mysqlConnector.videoExist(fileName)


	# check number of video in video folder
	# if number of video > config.numberofvideo wait 
	path, dirs, files = os.walk(videoPath).next()
	file_count = len(files)
	n = int(params['numberofvideo'])
	while n<=file_count:
		"""wait while video folder is overwhelmet"""	
		path, dirs, files = os.walk(r"F:\CIF\pistobribitka\videoLoader\video").next()
		file_count = len(files)
		print ("The number of files in the video folder has been exceeded. Finde : "+ str(file_count)+" files")
		time.sleep(int(params['timetocheckvideospaceisfree']))# waiting time before retesting
		
	if not videoId:
		"""download video if in database non-availability record"""
		print "video response"
		try:
			response = requests.get(file_path)
		except ChunkedEncodingError:
			return
		print "video responsed"
		with open(videoPath + fileName, 'wb') as f:
			print "video downloading"
			f.write(response.content)
		print "video downloaded"
		videoId = mysqlConnector.jsonToMySQLVideo(jsonVideo)
		rightToDB(jsonVideo, videoId)
		
		"""DELETING VIDEO FROM QUEUE"""
		ch.basic_ack(delivery_tag=method.delivery_tag)
		print "QUEUE element delete"
	else:
		"""write task data to DB if video record are availability"""
		print "video exists"
		rightToDB(jsonVideo, videoId)
		"""DELETING VIDEO FROM QUEUE"""
		ch.basic_ack(delivery_tag=method.delivery_tag)
		print "QUEUE element delete"


def getFileName(filePath):
	"""Receive file pass, and return file name"""
	index = filePath.rfind('/')
	fileName = filePath[index+1:]
	return fileName

def rightToDB(jsonToDB, videoId):
	"""right task parameters data to local MySQL database"""
	fileName = getFileName(jsonToDB['file_path'])
	lastTaskId =  mysqlConnector.jsonToMySQLTask(videoId,int(jsonToDB['id']))
	conf = jsonToDB['config']
	for o in conf:
		if str(o['type']) == 'line':
			"""right line location points to linelocation"""
			print "Location: " + str(o['type']) + str(o['points'])
			mysqlConnector.jsonToMySQLLine(lastTaskId, o)
		elif str(o['type']) == 'polygon':
			"""right zone location points to zonelocation"""
			print "right to db location: " + str(o['points'])
			mysqlConnector.jsonToMySQLZone(lastTaskId, o)


'''start server busy checking in separate thread'''
t = thread.Thread(target = checking, args=())
t.deamon = True
t.setName("CheckServerIsFree")
t.start()

'''queue checking'''
connector = Connection(host='vision.ecsv.org.ua', login='prosperodesu', password='s45fdfx65')
connector.addCallback('open_pose', callback_converter)
while True:
	try:
		connector.start()
	except:
		print "Except in connector.start()"