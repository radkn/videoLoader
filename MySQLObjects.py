import json

class MySQLVideo:
	def __init__(self, videoJSON):
		self.filePath = videoJSON['file_path']
		index = self.filePath.rfind('/')
		self.videoName = self.filePath[index+1:]
		self.id = videoJSON['id']
		self.screenPath = videoJSON['screen_path']
		self.screenWidth = videoJSON['screen_width']
		self.screenHeight = videoJSON['screen_height']

class MySQLLine:
	def __init__(self, jsonLine):
		self.rev_count = 0
		self.x1 = 0
		self.y1 = 0
		self.x2 = 0
		self.y2 = 0
		self.location = ""
