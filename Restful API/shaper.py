#!/usr/local/bin/python
# coding: utf-8

import MySQLdb, os, subprocess, socket, datetime
from flask import Flask
from flask import request
app = Flask(__name__)

db = MySQLdb.connect(host="localhost", user="root",passwd="######",db="######")
cursor = db.cursor()


ip = socket.gethostbyname(socket.gethostname())


@app.route('/',methods=['GET'])
def url():
	return "\n\nRequest Denied...<br>\nCheck your URL and try again...<br>\n\n"


@app.route('/interfaces', methods=['GET', 'POST'])
def ifaces():
	if (request.args.get('uname') == "######" and request.args.get('pass') == "######"):
		i = subprocess.check_output("ls /sys/class/net",shell=True)
		inter = i.splitlines()
		interfaces = "\n<br>".join(inter[0:])
		b = subprocess.check_output("brctl show", shell=True)
		bridge = b.splitlines()
		bridges = "	".join(bridge[0:])
		return "\nAvailabale Interfaces in shaper ("+ip+") are :<br>\n"+interfaces+"<br><br>\n\nAvailable Bridge Connections:<br>\n"+bridges
	else:
		return "Access denied... Authentication required..."

@app.route('/view_log', methods=['GET', 'POST'])
def view_log():
	if (request.args.get('uname') == "######" and request.args.get('pass') == "######"):
		with open("log.txt", "rb") as fo:
			data = "".join(fo.readlines()[0:])
			return data

@app.route('/traffic', methods=['GET', 'POST'])
def check_traffic():
	if (request.args.get('uname') == "######" and request.args.get('pass') == "######"):
		if(request.args.get('iface')):
			interface = request.args.get('iface')
			cmd = "sudo tc qdisc show dev "+interface
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
			
			return "Traffic on the interface ("+interface+") is as below:<br>\nDelay: "+delay_value+"<br>\nJitter: "+jitter_value+"<br>\nLoss: "+loss_value+"\n"
		else:
			return "<br><br>\n\nRequest Denied...<br>\nMention the interface on which traffic should be viewed and try again...<br><br>\n\n" 
	else:
		return "Access denied... Authentication required..."



@app.route('/shaping', methods=['GET', 'POST', 'DELETE'])
def traffic():
	if (request.args.get('uname') == "######" and request.args.get('pass') == "######"):
		if(request.args.get('iface')):
			interface = request.args.get('iface')
			dt = datetime.datetime.now()
			if (request.args.get('action') == "add"):
				action = "add"
				cmd1 = "sudo tc qdisc del dev " + interface + " root netem" 
				remove_traffic = os.system (cmd1)
				if (request.args.get('delay')):
					delay = request.args.get('delay')
				else: 
					delay = "0ms"
				if (request.args.get('loss')):
					loss = request.args.get('loss')
				else: 
					loss = "0%"
				if (request.args.get('jitter')):
					jitter = request.args.get('jitter')
				else: 
					jitter = "0ms"
				
				sql = 'create table IF NOT EXISTS `'+ip+'` (id int AUTO_INCREMENT PRIMARY KEY, delay varchar(15) DEFAULT "0ms", jitter varchar(15) DEFAULT "0ms", loss varchar(15) DEFAULT "0%", interface varchar(15))'
				cursor.execute(sql)
				db.commit()
				sql0 = 'select id from `'+ip+'` where interface="'+interface+'"'
				cursor.execute(sql0)
				row_num = cursor.fetchone()
				if (row_num):
					sql1 = 'update `'+ip+'` set delay="'+delay+'", jitter="'+jitter+'", loss="'+loss+'" where id= "'+str(row_num[0])+'"'
					cursor.execute(sql1)
					db.commit()
					
				else:
					sql1 = 'insert into `'+ip+'` (delay, jitter, loss, interface) values ("'+delay+'", "'+jitter+'", "'+loss+'", "'+interface+'")'
					cursor.execute(sql1)
					db.commit()
				cmd = "sudo tc qdisc add dev " + interface + " root netem delay " + delay +" "+ jitter+" loss " + loss
				comm = os.system (cmd) 
			

				return "<br>\n\nTraffic shaped successfully on "+interface+" in shaper ("+ip+")<br>\nTraffic on "+interface+" is as follows:<br>\ndelay:"+delay+"<br>\njitter:"+jitter+"<br>\nloss:"+loss+"\n\n" 

			elif (request.args.get('action') == "delete"):
				cmd = "sudo tc qdisc del dev " + interface + " root netem"
				comm = os.system(cmd)
				return "<br><br>\n\n Traffic successfully deleted on "+interface+" in shaper ("+ip+")<br>\n"
			else:
				return '<br>Enter proper action on the interface ' + interface
		else:
			return "<br>Enter the interface and try again ..."
	else:
		return "Access denied... Authentication required..."


@app.route('/ipfilter', methods=['GET', 'POST'])
def ipfilter():
	if (request.args.get('uname') == "######" and request.args.get('pass') == "######"):
		if (request.args.get('fip') and request.args.get('action')):
			ip = request.args.get('fip')
			action = request.args.get('action')
			if (action == "block"):			
				cmd1 = "sudo iptables -A INPUT -s "+ip+" -j DROP"
				cmd2 = "sudo iptables -A OUTPUT -s "+ip+" -j DROP"
				e1 = subprocess.check_output(cmd1, shell=True)
				e2 = subprocess.check_output(cmd2, shell= True)
				return "you entered ip: " + ip + "<br>\nfilter successfully added"
			elif (action == "unblock"):			
				cmd1 = "sudo iptables -D INPUT -s "+ip+" -j DROP"
				cmd2 = "sudo iptables -D OUTPUT -s "+ip+" -j DROP"
				e1 = subprocess.check_output(cmd1, shell=True)
				e2 = subprocess.check_output(cmd2, shell= True)
				return "you entered ip: " + ip + "<br>\nfilter successfully deleted"
			else:
				return "Unsupported Action... try again..."
		else:
			return "ip is not give in the arguments.... try again..."
	else:
		return "Access denied... Authentication required..."
	



if __name__ == '__main__':
   app.run('0.0.0.0')
