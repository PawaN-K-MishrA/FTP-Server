import sys
sys.path.append('..')
from data.DBConnection import DBConnection
class Authentication:
	@staticmethod
	def loginCheck(u,p):
		result=-1
		conx=DBConnection.connect()
		cur=conx.cursor()
		
		query='select userId,userName,password from userMaster'
		cur.execute(query)
		x=cur.fetchall()
		for i in x:
			if (i[1]==u and i[2]==p):
				return i[0]
		cur.close()
		conx.close()
		return result
	@staticmethod
	def forgot_password():
		pass
	@staticmethod
	def change_password(u,o,n):
		result=False
		conx=DBConnection.connect()
		cur=conx.cursor()
		query='select password from userMaster where userId=%s'
		value=(u,)
		cur.execute(query,value)
		x=cur.fetchall()
		for i in x:
			if (i[0]==o):
				result=True
				query='update userMaster set password=%s where userId=%s'
				value=(n,u)
				cur.execute(query,value)
		conx.commit()
		cur.close()
		conx.close()
		return result
		
		
	@staticmethod
	def logout():
		sys.exit()
		
			
		