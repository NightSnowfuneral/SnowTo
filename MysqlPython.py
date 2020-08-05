
import pandas as pd
import pymysql

config = {
	
	'host':'localhost',
	'user':'root',
	'password':'Cm393683462',
	'charset':'utf8',
	'port':'3306'
}

class MysqlHelp(object):
	def __init__(self,database='Cost',host="localhost",user='root',password='Cm393683462',port=3306):
		self.database = database
		self.host = host
		self.user = user
		self.password = password
		self.port = port
		self.conn = None
		
	def open(self):
		self.conn = pymysql.connect(host = self.host,user = self.user, password = self.password, database =self.database, port = self.port)
		self.cur = self.conn.cursor()
	def close(self):
		self.cur.close()
		self.conn.close()
	def getAll(self,sql):
		col=[]
		self.open()
		#self.cur.execute('select * from student where id=1') 
		self.cur.execute(sql)
		cols = self.cur.description
		columns = [col[0]for col in cols ]
		result = self.cur.fetchall()
		return[
			dict(zip(columns,row))
			for row in result 
			] 
		#result = self.cur.fetchall()
		
		#columns = pd.DataFrame(list(col))
		#df = pd.DataFrame(list(result),columns=columns[0])
		self.close()
		#print(result)
		#return result
		
		
	def add(self,sql,val):
		self.open()
		self.cur.executemany(sql,val)
		self.conn.commit()
		self.close()
		print(self.cur.rowcount,'success')
	def update(self,sql,val):
		self.open()
		self.cur.execute(sql,val)
		self.conn.commit()
		print("ok")
		self.close()
		print(self.cur.rowcount,'success')
	def delete(self,sql):
		self.open()
		self.cur.execute(sql)
		self.conn.commit()
		print("ok")
		self.close()
		print(self.cur.rowcount,"success")
		
			


#if __name__ == "__main__":
#	MysqlHelp()
		






