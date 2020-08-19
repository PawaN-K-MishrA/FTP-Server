class User:
	def __init__(self,userId=0,userName=0,password=0,userType=0,userStatus=0,name=0,email=0,contact=0,address=0,gender=0):
		self.__userId=userId
		self.__userName=userName
		self.__password=password
		self.__userType=userType
		self.__userStatus=userStatus
		self.__name=name
		self.__email=email
		self.__contact=contact
		self.__address=address
		self.__gender=gender
	def __str__(self):
		return str(self.__userId)+" "+str(self.__userName)+" "+str(self.__password)+" "+str(self.__userType)+" "+str(self.__userStatus)+" "+str(self.__name)+" "+str(self.__email)+" "+str(self.__contact)+" "+str(self.__address)+" "+str(self.__gender)
	def getUserId(self):
		return self.__userId
	def getUserName(self):	
		return self.__userName
	def getPassword(self):
		return self.__password
	def getUserType(self):
		return self.__userType
	def getUserStatus(self):
		return self.__userStatus
	def getName(self):
		return self.__name
	def getEmail(self):
		return self.__email
	def getContact(self):
		return self.__contact
	def getAddress(self):
		return self.__address
	def getGender(self):
		return self.__gender
	def setUserId(self,id):
		self.__userId=id
	def setUserName(self,userName):
		self.__userName=userName
	def setPassword(self,password):
		self.__password=password
	def setUserType(self,userType):
		self.__userType=userType
	def setUserStatus(self,userStatus):
		self.__userStatus=userStatus
	def setName(self,name):
		self.__name=name
	def setEmail(self,email):
		self.__email=email
	def setContact(self,contact):
		self.__contact=contact
	def setAddress(self,address):
		self.__address=address
	def setGender(self,gender):
		self.__gender=gender

		
		
		
		