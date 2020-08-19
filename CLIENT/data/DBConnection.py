import mysql.connector as mysql
class DBConnection:
	host='127.0.0.1'
	port=3306
	user='root'
	passwd='************'
	db='ftpserver'
	@staticmethod
	def connect():
		return mysql.connect(host=DBConnection.host,port=DBConnection.port,user=DBConnection.user,passwd=DBConnection.passwd,database=DBConnection.db)
 