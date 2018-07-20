# videoLoader
Video loader used to check queue, download file from it and writen data about task in DB (task, video parameters, zone and line location). 
Also, separate thread check for unsuccessful tasks and not sent data.

install:
	- install python 2.7;
	- install mysql-connector-python-2.0
	
	
first steps to use:
	- set config.ini parameters:
		*[mysql] - data base autorization parameters
		*[path] - path to video(for open pose) and JSONs(for new vision) local folders
		*[parameters] - numberofvideo(the maximum number of video files that can be located locally)
						timetocheckserverbusy(frequency to check server busy)
						timetocheckvideospaceisfree(frequency to check video space is free)
	- start mainLoader.py from cmd