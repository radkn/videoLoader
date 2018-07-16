import mysql.connector
from mysql.connector import Error, MySQLConnection
from config import read_config

def videoExist(videoName):
	"""checking match the name of the video in DB without extention"""
	db_config = read_config()
	videoName = videoName[:videoName.rfind('.')]
	ex = None
	try:
		conn = MySQLConnection(**db_config)
		if conn.is_connected():
			print 'Connected to', db_config['database']
		else:
			print 'conection failed'
		query = "SELECT * FROM video WHERE name='"+videoName+"'"
		video = conn.cursor()
		video.execute(query)
		row = video.fetchone()
		if row:
			ex = row[0]
	except Error as e:
		print(e)

	finally:
		conn.close()
		print 'Connection closed'
	return ex

def jsonToMySQLLine(profileId, jsonLine):
	"""right line location points to linelocation"""
	db_config = read_config()
	"""connect to MySQL DB"""
	try:
		conn = MySQLConnection(**db_config)
		if conn.is_connected():
			print 'Connected to', db_config['database']
		else:
			print 'conection failed'

		line = conn.cursor()
		query = ('INSERT INTO linelocation(task_id, location,x1, y1, x2, y2)')
		query += " VALUES (%s,%s,%s,%s,%s,%s)"
		args = (profileId, jsonLine['location'],
			jsonLine['points']['x1'],jsonLine['points']['y1'],
			jsonLine['points']['x2'],jsonLine['points']['y2'])
		line.execute(query, args)
		conn.commit()

	except Error as e:
		print(e)

	finally:
		conn.close()
		print 'Connection closed'

def jsonToMySQLZone(profileId, jsonZone):
	"""right zone location points to zonelocation"""
	db_config = read_config()
	"""connect to MySQL DB"""
	try:
		conn = MySQLConnection(**db_config)
		if conn.is_connected():
			print 'Connected to', db_config['database']
		else:
			print 'conection failed'

		line = conn.cursor()
		query = ('INSERT INTO zonelocation(task_id, location, point_number, x, y)')
		query += " VALUES (%s,%s,%s,%s,%s)"
		pointNum = 0
		for p in jsonZone['points']:
			args = (profileId, 'location', pointNum,
				p['x'],p['y'])
			line.execute(query, args)
			pointNum+=1
		conn.commit()

	except Error as e:
		print(e)

	finally:
		conn.close()
		print 'Connection closed'


def jsonToMySQLVideo(jsonVideo):
	"""right video parameters to video table"""
	fileName = getFileName(jsonVideo['file_path'])
	index = fileName.rfind('.')
	fileName = fileName[:index]
	db_config = read_config()
	lastid = 0
	"""connect to MySQL DB"""
	try:
		conn = MySQLConnection(**db_config)
		if conn.is_connected():
			print 'Connected to', db_config['database']
		else:
			print 'conection failed'
		video = conn.cursor()
		query = ('INSERT INTO video(name, file_path, screen_path, screen_width, screen_height, video_date)'
			+' VALUES(%s,%s,%s,%s,%s,%s)')

		"""temporary varriable to create different video name"""
		args = (fileName,jsonVideo["file_path"], jsonVideo["screen_path"],
			jsonVideo["screen_width"],jsonVideo["screen_height"], jsonVideo["video_date"])
		video.execute(query,args)

		if video.lastrowid:
			lastid = video.lastrowid
			print('last insert video id', video.lastrowid)
		else:
			lastid = 0
			print('last insert video id not found')

		conn.commit()
	except Error as e:
		print e
	finally:
		video.close()
		conn.close()
	return lastid


def jsonToMySQLTask(videoId, outsideId):
	"""right video parameters to video table"""
	db_config = read_config()
	lastid = 0
	"""connect to MySQL DB"""
	try:
		conn = MySQLConnection(**db_config)
		if conn.is_connected():
			print 'Connected to', db_config['database']
		else:
			print 'conection failed'
		profiles = conn.cursor()
		query = ('INSERT INTO task(video_id, outsidetask_id) VALUES(%s,%s)')

		args = (videoId,outsideId)
		profiles.execute(query,args)

		if profiles.lastrowid:
			lastid = profiles.lastrowid
			print('last insert task id', profiles.lastrowid)
		else:			
			print('last insert task id not found')

		conn.commit()
	except Error as e:
		print e
	finally:
		profiles.close()
		conn.close()
	return lastid


def getFileName(filePath):
	"""Receive file pass, and return file name"""
	index = filePath.rfind('/')
	fileName = filePath[index+1:]
	return fileName

def isNVLine():
	"""right zone location points to zonelocation"""
	db_config = read_config()
	"""connect to MySQL DB"""
	res = 1
	try:
		conn = MySQLConnection(**db_config)
		if conn.is_connected():
			print 'Connected to', db_config['database'], 'line'
		else:
			print 'conection failed'

		line = conn.cursor()
		query = ('SELECT COUNT(*) FROM line WHERE transmitted=0')
		line.execute(query)
		res = line.fetchone()[0]
		conn.commit()

	except Error as e:
		print(e)

	finally:
		conn.close()
		print 'Connecte to', db_config['database'], 'line closed'

	if res>0:
		return True
	else:
		return False


def isNVZone():
	"""right zone location points to zonelocation"""
	db_config = read_config()
	"""connect to MySQL DB"""
	res = 1
	try:
		conn = MySQLConnection(**db_config)
		if conn.is_connected():
			print 'Connected to', db_config['database'], 'zone'
		else:
			print 'conection failed'

		line = conn.cursor()
		query = ('SELECT COUNT(*) FROM zone WHERE transmitted=0')
		line.execute(query)
		res = line.fetchone()[0]
		conn.commit()

	except Error as e:
		print(e)

	finally:
		conn.close()
		print 'Connecte to', db_config['database'], 'zone closed'

	if res>0:
		return True
	else:
		return False

def isNotCimpleteTask():
	"""right zone location points to zonelocation"""
	db_config = read_config()
	"""connect to MySQL DB"""
	# res = True
	try:
		conn = MySQLConnection(**db_config)
		if conn.is_connected():
			print 'Connected to', db_config['database'], 'task'
		else:
			print 'conection failed'

		line = conn.cursor()
		query = ('SELECT COUNT(*) FROM task WHERE completed=0')
		line.execute(query)
		res = line.fetchone()[0]
		conn.commit()

	except Error as e:
		print(e)
	finally:
		conn.close()
		print 'Connecte to', db_config['database'], 'task closed'

	if res>0:
		return True
	else:
		return False
# connect()
