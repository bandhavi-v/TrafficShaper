# this file is to detect the traffic that has been changed through shaper console 

#!/usr/bin/python

import MySQLdb, os, subprocess, socket, time, datetime

#to get the ip address of the host
ip = socket.gethostbyname(socket.gethostname())

db = MySQLdb.connect("localhost","root","######","######" )
cursor = db.cursor()



def check_old_values():
	sql = 'SELECT id from `'+ip+'` where interface = "'+iface+'"'
	cursor.execute(sql)
	result = cursor.fetchone()
	if (result):
		sql = 'SELECT delay,jitter,loss FROM `'+ip+'` where interface = "'+iface+'"'
		cursor.execute(sql)
   		results = cursor.fetchall()
		if (results):
   			for row in results:
      				odelay = row[0]
      				ojitter = row[1]
      				oloss = row[2]
				fo = open("log.txt", "ab+")
				dt = datetime.datetime.now()
				line2 = "Date and Time :: "+str(dt)+"\n\n<br><br>"
				line3 = "Traffic Shaped on interface: "+iface+"\n<br>"
      				if (odelay != delay_value):	
      					sql_d = 'update `'+ip+'` set delay = "'+delay_value+'" where interface = "'+iface+'"'
      					cursor.execute(sql_d)
					db.commit()
					fo.write("\n\n\n<br><br><br>-------------------\n<br>")
					fo.write(line2)
					fo.write(line3)
      					if (oloss != loss_value):	
      						sql_l = 'update `'+ip+'` set loss = "'+loss_value+'" where interface = "'+iface+'"'
      						cursor.execute(sql_l)
						db.commit()
      						if (ojitter != jitter_value):	
      							sql_j = 'update `'+ip+'` set jitter = "'+jitter_value+'" where interface = "'+iface+'"'
      							cursor.execute(sql_j)
							db.commit()
					line4 = "Delay: "+delay_value+"\n<br>jitter:"+jitter_value+"\n<br>loss: "+loss_value+"\n<br>"
					fo.write(line4)
					line5 = "-------------------"
					fo.write(line5)
					fo.close()
				elif (oloss != loss_value):	
      					sql_l = 'update `'+ip+'` set loss = "'+loss_value+'" where interface = "'+iface+'"'
      					cursor.execute(sql_l)
					db.commit()
					fo.write("\n\n\n<br><br><br>-------------------\n<br>")
					fo.write(line2)
					fo.write(line3)
      					if (ojitter != jitter_value):	
      						sql_j = 'update `'+ip+'` set jitter = "'+jitter_value+'" where interface = "'+iface+'"'
      						cursor.execute(sql_j)
						db.commit()
					line4 = "Delay: "+delay_value+"\n<br>jitter:"+jitter_value+"\n<br>loss: "+loss_value+"\n<br>"
					fo.write(line4)
					line5 = "-------------------"
					fo.write(line5)
					fo.close()
				elif (ojitter != jitter_value):	
      					sql_j = 'update `'+ip+'` set jitter = "'+jitter_value+'" where interface = "'+iface+'"'
      					cursor.execute(sql_j)
					db.commit()
					fo.write("\n\n\n<br><br><br>-------------------\n<br>")
					fo.write(line2)
					fo.write(line3)
					line4 = "Delay: "+delay_value+"\n<br>jitter:"+jitter_value+"\n<br>loss: "+loss_value+"\n<br>"
					fo.write(line4)
					line5 = "-------------------"
					fo.write(line5)
					fo.close()
				else:
					message = "NOTHING TO CHECK IN THIS LOOP GO TO OTHER CONDITIONAL STATEMENT"

while (True):
	interfaces = subprocess.check_output("ls /sys/class/net",shell=True)
	ifaces = []
	ifaces = interfaces.splitlines()
	for iface in ifaces:

		cmd = "sudo tc qdisc show dev "+iface
		
		i = subprocess.check_output(cmd,shell=True)
		
		j = i.split(' ')
   		d,l,jtr = "delay","loss",10
    		if d in j:
        		a = j.index('delay')
        		a = a + 1
        		delay_value = j[a] 
        		if jtr < len(j):
            			if j[jtr] != "loss":
					jtr = jtr + 1
                			jitter_value = j[jtr] 
			else:
				jitter_value = "0ms"
		else:
			delay_value = "0ms"
			jitter_value = "0ms"
    		if l in j:
        		b = j.index('loss')
       			b = b + 1
       			loss_value = j[b] 
		else:
			loss_value = "0%"
		sql = 'create table IF NOT EXISTS `'+ip+'` (id int AUTO_INCREMENT PRIMARY KEY, delay varchar(15) DEFAULT "0ms", jitter varchar(15) DEFAULT "0ms", loss varchar(15) DEFAULT "0%", interface varchar(15))'
		cursor.execute(sql)
		db.commit()
		if (delay_value == "0ms" and jitter_value == "0ms" and loss_value == "0%"):
			sql = 'SELECT id from `'+ip+'` where interface = "'+iface+'"'
			cursor.execute(sql)
			result = cursor.fetchone()
			if (result):
				check_old_values()
				
		else:
			sql = 'SELECT id from `'+ip+'` where interface = "'+iface+'"'
			cursor.execute(sql)
			result = cursor.fetchone()
			if (result):
				check_old_values()
						
			else:
				sql1 = 'insert into `'+ip+'` (delay, jitter, loss, interface) values ("'+delay_value+'", "'+jitter_value+'", "'+loss_value+'", "'+iface+'")'
				cursor.execute(sql1)
				db.commit()
				fo = open("log.txt", "ab+")
				line1 = "\n\n\n<br><br><br>-------------------\n<br>"
				dt = datetime.datetime.now()
				line2 = "Date and Time :: "+str(dt)+"\n\n<br><br>"
				line3 = "Traffic Shaped on interface: "+iface+"\n<br>"
				line4 = "Delay: "+delay_value+"\n<br>jitter:"+jitter_value+"\n<br>loss: "+loss_value+"\n<br>"
				line5 = "-------------------" 
				log = line1+line2+line3+line4+line5
				fo.write(log);
				fo.close()
	time.sleep(3)

db.close()
