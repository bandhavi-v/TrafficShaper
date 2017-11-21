#!/usr/bin/python

import MySQLdb, time, subprocess, socket

db = MySQLdb.connect(host="localhost", user="root",passwd="######",db="######")
cursor = db.cursor()

ip = socket.gethostbyname(socket.gethostname())
# to know the shaper ip address

def discovery():
	if (iface != "lo"):
		if iface in data:
			e = "NOTHING THE INTERFACE IS PRESENT"
		else:
			sql = 'insert into `'+ip+'` (interface, delay, jitter, loss) VALUES ("'+iface+'", "0ms", "0ms", "0%")'
			cursor.execute(sql)
			db.commit()

while (True):
	cmd = subprocess.check_output("ls /sys/class/net", shell=True)
	interfaces = cmd.splitlines()
	for iface in interfaces:
		sql = 'select interface from `'+ip+'`'
		cursor.execute(sql)
		data = cursor.fetchall()
		if (data):
			discovery()
			
		else:
			sql = 'create table IF NOT EXISTS `'+ip+'` (id int AUTO_INCREMENT PRIMARY KEY, delay varchar(15) DEFAULT "0ms", jitter varchar(15) DEFAULT "0ms", loss varchar(15) DEFAULT "0%", interface varchar(15))'
			cursor.execute(sql)
			db.commit()
			discovery()
	#print "loop done\n"
	time.sleep(15)


 
	
		
