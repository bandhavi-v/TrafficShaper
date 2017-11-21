from flask import Flask, redirect, url_for, render_template, request, session
import os, subprocess, MySQLdb, datetime
app = Flask(__name__)

db = MySQLdb.connect(host="localhost", user="root",passwd="#####",db="######")
cursor = db.cursor()

app.secret_key = 'hello'
@app.route('/controller')
def index():
   return render_template('login_proj.html')

@app.route('/title.html')
def title_page():
	return render_template('title.html')

@app.route('/profile.html')
def profile_page():
	return render_template('profile.html')

@app.route('/indexed.html')
def indexed_page():
	return render_template('index.html')

@app.route('/display.html')
def display_page():
	return render_template('display.html')

@app.route('/view_int.html')
def view_int_page():
	return render_template('view_int.html')

@app.route('/view_traffic.html')
def view_traffic_page():
	return render_template('view_traffic.html')

@app.route('/change_traffic.html')
def change_traffic_page():
	return render_template('change_traffic.html')

@app.route('/delete_traffic.html')
def delete_traffic_page():
	return render_template('delete_traffic.html')

@app.route('/ip_filter.html')
def ip_filter_page():
	return render_template('ip_filter.html')

@app.route ('/view_log.html')
def view_log_page():
	return render_template('view_log.html')

@app.route('/dialhome',methods=['GET', 'POST'])
def dialhome():
	if (request.args.get('uname') == "######" and request.args.get('pass') == "######"):
		i = datetime.datetime.now()
		req_ip = request.remote_addr
		sql = "create table IF NOT EXISTS shaperpool (id int AUTO_INCREMENT PRIMARY KEY, ip_addr varchar(15), active_since varchar(54))"
		cursor.execute(sql)
		db.commit
		sql1 = 'select id from shaperpool where ip_addr="'+str(req_ip)+'"'
		cursor.execute(sql1)
		data = cursor.fetchone()
		if (data):
			sql2 = 'update shaperpool set ip_addr="'+str(req_ip)+'", active_since="'+str(i)+'" where id="'+str(data[0])+'"'
			cursor.execute(sql2)
			db.commit()
		else:
			sql2 = 'insert into shaperpool (ip_addr, active_since) VALUES ("'+str(req_ip)+'", "'+str(i)+'")'
			cursor.execute(sql2)
			db.commit() 
		return 'noted!\n<br>'

@app.route ('/main')
def main():
	if 'login' in session:
		return render_template('main.html')


@app.route('/login', methods=['GET', 'POST']) 
def login():
	
	if 'login' in session:
		return render_template('main.html')

	elif request.method == 'POST' or request.method == 'GET':
	 	user = request.form['uname']
	 	code = request.form['pwd']
	 	if user == "######" and code == "######":
	 		session['login'] = 'True'
	 		session['user'] = user
	 		session['pass'] = code
	 		return render_template('main.html')
	
	else:
		return redirect(url_for('index')) 
		

@app.route('/change_traffic', methods=['GET', 'POST'])
def change_traffic():
	if 'login' in session:
		ip = request.form['ip']
		iface = request.form['iface']
		if (request.form['dlay']):
			delay = request.form['dlay']
		else:
			delay = "0ms"
		if (request.form['loss']):
			loss = request.form['loss']
		else:
			loss = "0%"
		if (request.form['jitter']):
			jitter = request.form['jitter']
		else:
			jitter = "0ms"
		cmd = 'curl -X POST "http://'+ip+':5000/shaping?uname='+session['user']+'&pass='+session['pass']+'&action=add&iface='+iface+'&delay='+delay+'&jitter='+jitter+'&loss='+loss+'"'
		e = subprocess.check_output(cmd, shell=True)
		return e
	else:
		return redirect(url_for('index'))

@app.route('/view_traffic', methods=['GET', 'POST'])
def view_traffic():
	if 'login' in session:
		ip = request.form['ip']
		iface = request.form['iface']
		cmd = 'curl -X GET "http://'+ip+':5000/traffic?uname='+session['user']+'&pass='+session['pass']+'&iface='+iface+'"'
		e = subprocess.check_output(cmd, shell=True)
		return e
	else:
		return redirect(url_for('index'))


@app.route('/delete_traffic', methods=['GET', 'POST'])
def delete_traffic():
	if 'login' in session:
		ip = request.form['ip']
		iface = request.form['iface']
		cmd = 'curl -X DELETE "http://'+ip+':5000/shaping?uname='+session['user']+'&pass='+session['pass']+'&action=delete&iface='+iface+'"'
		e = subprocess.check_output(cmd, shell=True)
		return e
	else:
		return redirect(url_for('index'))

@app.route('/view_int', methods=['GET', 'POST'])
def interfaces():
	if 'login' in session:
		ip = request.form['ip']
		cmd = 'curl -X GET "http://'+ip+':5000/interfaces?uname='+session['user']+'&pass='+session['pass']+'"'
		e = subprocess.check_output(cmd, shell=True)
		return e
	else:
		return redirect(url_for('index'))

@app.route('/available_nodes')
def available_nodes():
	if 'login' in session:
		query = "SELECT * from shaperpool"
        	cursor.execute(query)
       		data = cursor.fetchall()
		return render_template("dashboard.html", data=data)
		return data
	else:
		return redirect(url_for('index'))


@app.route('/bouip', methods=['POST', 'GET'])
def filter():
	if 'login' in session:
		if (request.form['ip'] and request.form['action'] and request.form['fip']):
			ip = request.form['ip']
			action = request.form['action']
			fip = request.form['fip']
			cmd = 'curl -X POST "http://'+ip+':5000/ipfilter?uname='+session['user']+'&pass='+session['pass']+'&action='+action+'&fip='+fip+'"'
			e = subprocess.check_output(cmd, shell=True)
			return e
	else:
		return redirect(url_for('index'))

@app.route('/view_log', methods=['POST', 'GET'])
def view_log():
	if (request.form['ip']):
		ip = request.form['ip']
		cmd = 'curl -X GET "http://'+ip+':5000/view_log?uname='+session['user']+'&pass='+session['pass']+'"'
		e = subprocess.check_output(cmd, shell=True)
		return e

@app.route('/home')
def home():
	if 'login' in session:
		return render_template('main.html')
	else:
	 	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	session.pop('user', None)
	session.pop('pass', None)
	session.pop('login', None)
	return redirect(url_for('index'))
				
if __name__ == '__main__':
   app.run(host= '0.0.0.0', port = '5001')
