import pika
import sys
 
 
class Connection:
	def __init__(self, host, login, password,):
		credentials = pika.PlainCredentials(login, password)
		parameters = pika.ConnectionParameters(credentials=credentials, host=host)
		self.connection = pika.BlockingConnection(parameters=parameters)
		self.channel = self.connection.channel()
		self.queueList = []
 
	def on_open_connection(self, connection):
		print "Coooooonnnnection open"
		print connection
 
	def on_open_channel(self, channel):
		print "Chaaaaaannel open"
		print channel
 
	def addCallback(self, queue, callback):
		data = {"queue": queue, "callback": callback}
		self.queueList.append(data)
 
	def start(self):
		
		try:
			# Loop so we can communicate with RabbitMQ
			# set up subscription on the queue
			if len(self.queueList) > 0:
				for item in self.queueList:
					print self.channel.basic_get(item['queue'])
					self.channel.basic_consume(item['callback'],
											   queue=item['queue'])
				self.channel.start_consuming()
			else:
				print 'Not found queues'
				sys.exit()
		except KeyboardInterrupt:
			print "exception in try of start function"
			# Gracefully close the connection
			self.connection.close()
			# Loop until we're fully closed, will stop on its own
			self.channel.start_consuming()

