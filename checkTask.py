import time
import pika
import json

# local
import mysqlConnector
from config import read_config

def queueToServer():

	message = json.dumps([{'message':'Server is free'}])
	queue = "task_completed"
	credentials = pika.PlainCredentials('prosperodesu', 's45fdfx65')
	connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=credentials,
	        host='vision.ecsv.org.ua'))
	channel = connection.channel()

	channel.queue_declare(queue=queue, durable = True)

	channel.basic_publish(exchange='',
	                      routing_key=queue,
	                      body=message)
	print " [x] Sent 'massage is sent'"
	connection.close()

def checking():
	while True:
		t = mysqlConnector.isNotCimpleteTask()
		l = mysqlConnector.isNVLine()
		z = mysqlConnector.isNVZone()
		isFree = not (t or l or z)
		print ">>>>Server is free: ", isFree
		if isFree:
			queueToServer()
		sleepTime = int(read_config(section='parameters')['timetocheckserverbusy'])
		time.sleep(sleepTime)

		print "Not comtleted task",t
		print "Line records",l
		print "Zone records",z