from flask import   Flask, jsonify, abort, request,flash
from flask_cors import CORS
from MysqlPython import MysqlHelp
from io import StringIO
from datetime import date
import uuid
import json
import pymysql
import datetime
import pandas as pd
import os
from werkzeug.utils import secure_filename
import chardet  
app = Flask('test')
app.config['UPLOAD_FOLDER'] = '/root/snow/dist/pdf'
CORS(app)
configLocal = 'http://172.16.10.20:5678/pdf/'
mysql = MysqlHelp()
ALLOW_EXTENSIONS = set(['html', 'htm', 'doc', 'docx', 'mht', 'pdf','txt'])
cmde = {'name':'6'}
def allowed_file(filename):
 return '.' in filename and \
   filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS

def AccomDatae(filename):
	if filename == '001':
		return '是'
	if filename == '002':
		return '否'
class nava:     
	def data(allnav,power):
		print (allnav)
		jsonData = []
		if power=='ptyh':
			return allnav[0]
		if power=='zsyh':
			return allnav[1]
		else:
			return allnav[2]	
			
		
		
		

@app.route('/nav')
def hello():
	args = request.args.get("power")
	
	sql_select = ("SELECT * FROM Tit_Name")
	rv = mysql.getAll(sql_select)
	jsonData = []
	data = nava.data(rv,args)
	print(data)
	return jsonify(data)	
	
       
#	for result in rv:
#		content = {'id':result[0],'username':result[1],'password': result[2]}
#
#		payload.append(content)
#		content{}
#	return jsonify(payload)


@app.route('/settle')
def SettData():
	args = request.args.get("data")
	return jsonify(args)

	
@app.route('/session',methods=['POST','GET'])
def post():
	recv_data = request.get_json()
	print(recv_data)
	username = recv_data['phone']
	password = recv_data['password']

	
	sql_select = ("SELECT * FROM student WHERE username='%s' and password='%s'") % (username,password)
	sql_select_power = ("select power from student where username='%s' and password = '%s' " ) % (username,password)
	rv = mysql.getAll(sql_select)
	jsonData=[]
	for row in rv:
		result = {}
		result['power'] = row[5]
		jsonData.append(result)
	
	print(jsonData)
	if not rv == (): 
		return jsonify({'code':200,'data':jsonData})
	else:
		return jsonify({'code':403})
	
	print(rv)
	return jsonify(rv)
@app.route('/home')
def Hello():
	args = request.args.get("power")
	sql_select = (" select * from Tit_Name where power='%s' " % args)
	rv = mysql.getAll(sql_select)
	print(rv)
	return jsonify(rv)
	
@app.route('/goback/<int:year>')
def go_back(year):
	return '<p>Welocome to %d</p>' %(2018 -year)

@app.route('/records')
def records():
	args = request.args.get('status')
	sql_select = (" select * from Project_Name,PQZ_Data where P_id = Pj_id")
	rv = mysql.getAll(sql_select)
	
	return jsonify(rv)

@app.route('/search/resource')
def resource():
	
	sql_select = (" select * from Project_Name,PQZ_Data where P_id = Pj_id")
	rv = mysql.getAll(sql_select)
	
	return jsonify(rv)

@app.route('/Organization')
def Organize():
	
	sql_select = (" select * from Project_Name")
	
	rv = mysql.getAll(sql_select)
	return jsonify(rv)


@app.route('/ManageAddData',methods=['POST','GET'])
def ManageAddDataOPts():
		recv_data = request.get_json('data')
		sql_select = ("INSERT INTO  PQZ_Data(qzbh,dfdw,qznr,xxnr,file,Accom,qzje,qzsj,yyfx,bz,Pj_id,statusID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		qzhb = recv_data['qxdj']
		dfdw = recv_data['Dfdw']
		qznr = recv_data['description']
		xxnr = recv_data['stationID']
		file = configLocal + recv_data['file']
		Accom = AccomDatae(recv_data['AccomData'])
		qzje = recv_data['qxlx']
		qzsj = recv_data['DefectsTime']
		yyfx = recv_data['stationID']
		bz   = recv_data['Bzhu']
		Pj_id = recv_data['createUserName']
		statusID = recv_data['statusID']
		value = [(qzhb,dfdw,qznr,xxnr,file,Accom,qzje,qzsj,yyfx,bz,Pj_id,statusID)]
		print(value)
		rv = mysql.add(sql_select,value)
		print(rv)
		return jsonify({"status":200,"info":"新增数据成功"})
		
@app.route('/ManageEditData',methods=['POST','GET'])
def ManageEditDataOpts():
		recv_data = request.get_json('data')
		print(recv_data)
		qzid = recv_data['qz_id']
		qzhb = recv_data['qxdj']
		dfdw = recv_data['Dfdw']
		qznr = recv_data['description']
		xxnr = recv_data['stationID']
		file = configLocal + recv_data['file']
		Accom = AccomDatae(recv_data['AccomData'])
		qzje = recv_data['qxlx']
		qzsj = recv_data['DefectsTime']
		yyfx = recv_data['description']
		bz   = recv_data['Bzhu']
		Pj_id = recv_data['createUserName']
		
		sql_select = ("UPDATE PQZ_Data SET qzbh = %s,dfdw = %s,qznr = %s,xxnr = %s, file = %s, Accom = %s,qzje = %s, qzsj=%s, yyfx =%s,bz=%s,Pj_id = %s  WHERE qz_id = %s") 
		value = (qzhb,dfdw,qznr,xxnr,file,Accom,qzje,qzsj,yyfx,bz,Pj_id,qzid)
		rv = mysql.update(sql_select,value)
		return jsonify({"status":200,"info":"修改数据成功"})
		
@app.route('/uploader',methods=['POST','GET'])
def uploader():
	if request.method == 'POST':
		print(os.getcwd())
		if 'file' not in request.files:
			return  jsonify({"status":500,"info":"文件上传不成功"})
		file = request.files['file']
		if file and allowed_file(file.filename):	
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
			return  jsonify({"status":200,"info":"文件上传成功"})
@app.route('/tasks', methods=['GET','POST'])
def Tasks():
	 recv_data = request.args.get("id")
	 sql_select = (" select * from PQZ_Data where qz_id = %s" % recv_data)
	 rv = mysql.getAll(sql_select)
	 return jsonify(rv) 

@app.route('/shift_record/<user_id>',methods=['POST','GET'])
def shift_recordOpts(user_id):
	recv_data = user_id
	sql_select = ("DELETE FROM PQZ_Data where qz_id = %s" % recv_data)
	rv = mysql.delete(sql_select)
	return jsonify({"status":200,"info":"删除数据成功"})
@app.route('/search/records',methods=['POST','GET'])
def SearchRecords():
	recv_data = request.get_json('data')
	sql_select = ""
	sql_Data=""
	name = []
	keys = []
	if recv_data['status']  == '0':
		sql_select = ("select * from PQZ_Data ")
		
	else:
		for a in recv_data:
			if recv_data[a] != None:
				if a == "Accom":
					name.append(a)	
					keys.append(AccomDatae(recv_data[a]))
				else:
					name.append(a)	
					keys.append(recv_data[a])
				

			
		dictionary = dict(zip(name,keys))
		print(dictionary)
		if len(dictionary) ==1:
			sql_select = ("select * from PQZ_Data ")
		if len(dictionary) ==2:
			for a in dictionary:
				if a != 'status':
					
					if a == 'Accom' or a == 'dfdw':
						sql_Data = (a + ' = ' + "'%s'") % (dictionary[a])
					if a == 'qzsj':
						sql_Data += (a+' '+'between'+' '+ "'%s'" + ' and ' + "'%s'")%(dictionary[a][0],dictionary[a][1])
					if a == 'Pj_id':
						sql_Data =(a + ' = ' + '%s') % (dictionary[a])
						
			sql_select = ("""select * from PQZ_Data where %s""" ) % (sql_Data)	
		if len(dictionary) >2:
			for a in dictionary:
				if a != 'status':
					if a == 'Accom' or a == 'dfdw':
						sql_Data += (' and ' + a + ' = ' + "'%s'") % (dictionary[a])
					if a == 'qzsj':
						sql_Data += (' and ' + a +' '+'between'+' '+ "'%s'" + ' and ' + "'%s'")%(dictionary[a][0],dictionary[a][1])
					if a == 'Pj_id':
						sql_Data +=(' and ' + a + ' = ' + '%s') % (dictionary[a])	
			sql_Data = sql_Data.strip(' and ')
			
			sql_select = ("""select * from PQZ_Data where %s""" ) % (sql_Data)
			print(sql_select)
	rv = mysql.getAll(sql_select)
	return jsonify(rv)


if __name__ == "__main__":
	app.run(host="0.0.0.0",port=3652,debug=True)
