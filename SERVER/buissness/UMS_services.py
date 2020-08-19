import sys
sys.path.append('..')
from data.DBConnection import DBConnection
from data.user import User
class UMS_services:
	@staticmethod
	def add(u):
		result=False
		conx=DBConnection.connect()
		cur=conx.cursor()
		query='insert into userMaster (userName,password,userType,userStatus,name,email,contact,address,gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		data=[]
		data.append(u.getUserName())
		data.append(u.getPassword())
		data.append(u.getUserType())
		data.append(u.getUserStatus())
		data.append(u.getName())
		data.append(u.getEmail())
		data.append(u.getContact())
		data.append(u.getAddress())
		data.append(u.getGender())
		try:
			cur.execute(query,data)
		except:
			conx.commit()
			cur.close()
			conx.close()
			return result
		if (cur.rowcount==1):
			result=True
		conx.commit()
		cur.close()
		conx.close()
		return result
	@staticmethod
	def view():
		conx=DBConnection.connect()
		cur=conx.cursor()
		query='select * from userMaster'
		y=[]
		cur.execute(query)
		x=cur.fetchall()
		for i in x:	
			u=User()
			u.setUserId(i[0])
			u.setUserName(i[1])
			u.setPassword(i[2])
			u.setUserType(i[3])
			u.setUserStatus(i[4])
			u.setName(i[5])
			u.setEmail(i[6])
			u.setContact(i[7])
			u.setAddress(i[8])
			u.setGender(i[9])
			y.append(u)
		conx.commit()
		conx.close()
		cur.close()
		return y
	@staticmethod
	def search(id):
		conx=DBConnection.connect()
		cur=conx.cursor()
		query='select * from userMaster where userId=%s'
		value=(id,)
		cur.execute(query,value)
		x=cur.fetchall()
		u=User()
		for i in x:
			u.setUserId(i[0])
			u.setUserName(i[1])
			u.setPassword(i[2])
			u.setUserType(i[3])
			u.setUserStatus(i[4])
			u.setName(i[5])
			u.setEmail(i[6])
			u.setContact(i[7])
			u.setAddress(i[8])
			u.setGender(i[9])
		conx.commit()
		cur.close()
		conx.close()
		return u
	@staticmethod
	def update(u):
		result=False
		conx=DBConnection.connect()
		cur=conx.cursor()
		data=[]
		query='update userMaster set userType=%s,userStatus=%s,name=%s,email=%s,contact=%s,address=%s,gender=%s where userId=%s'
		data.append(u.getUserType())
		data.append(u.getUserStatus())
		data.append(u.getName())
		data.append(u.getEmail())
		data.append(u.getContact())
		data.append(u.getAddress())
		data.append(u.getGender())
		data.append(u.getUserId())
		cur.execute(query,data)
		if (cur.rowcount==1):
			result=True
		conx.commit()
		cur.close()
		conx.close()
		return result
	@staticmethod
	def updateProfile(u,x):
		result=False
		conx=DBConnection.connect()
		cur=conx.cursor()
		data=[]
		query='update userMaster set name=%s,email=%s,contact=%s,address=%s,gender=%s where userId=%s'
		data.append(u.getName())
		data.append(u.getEmail())
		data.append(u.getContact())
		data.append(u.getAddress())
		data.append(u.getGender())
		data.append(x)
		cur.execute(query,data)
		if (cur.rowcount==1):
			result=True
		conx.commit()
		cur.close()
		conx.close()
		return result
	@staticmethod	
	def insertfile(u,x,y):
		result=False
		conx=DBConnection.connect()
		cur=conx.cursor()
		query='insert into userfiles values(%s,%s,%s)'
		values=(u,x,y)
		cur.execute(query,values)
		if (cur.rowcount!=0):
			result=True
		conx.commit()
		cur.close()
		conx.close()
		return result
	@staticmethod
	def deletefile(i,u):
		result=False
		conx=DBConnection.connect()
		cur=conx.cursor()
		print(u)
		print(i)
		query='delete from userfiles where filename=%s and userid=%s'
		value=(i,u)
		cur.execute(query,value)
		if (cur.rowcount==1):
			result=True
		conx.commit()
		cur.close()
		conx.close()
		return result
	@staticmethod
	def change_file_name(n_fname,userid,o_fname):
		result=False
		conx=DBConnection.connect()
		cur=conx.cursor()
		query='update userfiles set filename=%s where userid=%s and filename=%s'
		value=(n_fname,userid,o_fname)
		cur.execute(query,value)
		if (cur.rowcount==1):
			result=True
		conx.commit()
		cur.close()
		conx.close()
		return result
			
			
		
		
		
		
		
		
		
			
			