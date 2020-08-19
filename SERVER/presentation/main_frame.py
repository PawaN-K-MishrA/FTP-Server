import sys
sys.path.append('..')
import tkinter as tk
from login import A
import os
from tkinter import messagebox
from buissness.login_services import Authentication
from buissness.UMS_services import UMS_services
from data.user import User
import socket
from threading import Thread
import time
class B:
	def __init__(self,w,utype):
		self.userid=w
		self.usertype=utype
		self.root=tk.Tk()
		self.root.title('FTP Server')
		self.root.geometry('500x400')
		
		self.menubar=tk.Menu(self.root)
		self.logoutmenu=tk.Menu(self.menubar,tearoff=0)
		self.logoutmenu.add_command(label='logout',command=self.out)
		self.logoutmenu.add_command(label='change password',command=self.back1)
		self.menubar.add_cascade(label='logout',menu=self.logoutmenu)
		self.umsmenu=tk.Menu(self.menubar,tearoff=0)
		self.umsmenu.add_command(label='manage user',command=self.back2)
		self.umsmenu.add_command(label='manage profile',command=self.back3)
		self.menubar.add_cascade(label='UMS',menu=self.umsmenu)
		self.ftpmenu=tk.Menu(self.menubar,tearoff=0)
		self.ftpmenu.add_command(label='Start Server',command=self.back4)
		self.ftpmenu.add_command(label='Stop Server')
		self.menubar.add_cascade(label='SERVER',menu=self.ftpmenu)
		self.root.config(menu=self.menubar)
		self.root.mainloop()
		
	def back4(self):	
		Startserver()

	def out(self):
		Authentication.logout()
		A()
	
	def back1(self):
		self.root.destroy()
		Change_password(self.userid)
	
	def back2(self):
		self.root.destroy()
		manage_user(self.userid,self.usertype)
	
	def back3(self):
		self.root.destroy()
		manage_profile(self.userid,self.usertype)
	
	def back5(self):
		pass
		
class Startserver:

	def __init__(self):
		self.root=tk.Tk()
		self.root.title('Start Server')
		self.root.geometry('300x150')
		tk.Label(self.root,text='Enter Port number').grid(row=0,column=0,padx=10,pady=10)
		self.pt=tk.Entry(self.root)
		self.pt.grid(row=0,column=1)
		self.st=tk.Button(self.root,text='Start',width=15,command=self.start)
		self.st.grid(row=1,column=1)
		self.root.mainloop()
		
	
	def start(self):
		self.s=socket.socket()
		self.s.bind(('',int(self.pt.get())))
		self.s.listen(10)
		tk.Label(self.root,text='waiting for client....').grid(row=2,column=1)
		self.st.config(state='disabled')
		self.pt.config(state='disabled')
		self.t1=Thread(target=self.waitclient)
		self.t1.start()
		
		
	def waitclient(self):
		i=1
		while i<=10:
			self.conn,self.addr=self.s.accept()
			tk.Label(self.root,text='connected to'+str(self.addr)).grid(row=3,column=1)
			c=Options(self.conn)
			c.start()
			i+=1
	#def recive_file(self,c):
	#def send_file(self,conn):
	#def re_move_file(self,conn):
	#def re_name_file(self,conn):
		
		
class Options(Thread):
	def __init__(self,conn):	
		Thread.__init__(self)
		self.conn=conn
	
	def recv_file(self,conn):
		os.chdir('uploaded_files')
		self.conn.send(('Send username').encode('latin-1'))
		username=self.conn.recv(1024).decode('latin-1')
		if (os.path.exists(username)==False):
			os.mkdir(username)
		os.chdir(username)
		self.conn.send(('Send userid').encode('latin-1'))
		userid=self.conn.recv(1024).decode('latin-1')
		self.conn.send(('Send nof').encode('latin-1'))
		nof=self.conn.recv(1024).decode('latin-1')
		print(nof)
		self.conn.send(('Send filesize').encode('latin-1'))
		
		for i in range(int(nof)):
			filesize=self.conn.recv(1024).decode('latin-1')
			print(filesize)
			self.conn.send(('Send filename').encode('latin-1'))
			filename=self.conn.recv(1024).decode('latin-1')
			a=filename
			j=1
			while True:
				if (os.path.exists(filename)):
					nf=os.path.splitext(a)
					filename=nf[0]+str(j)+nf[1]
					j+=1
				else:
					break
			self.conn.send(('filename recived').encode('latin-1'))
			f=open(filename,'wb')
			print('file opned')
			data1=self.conn.recv(4096)
			while (data1):
				#print('server data writen')
				f.write(data1)
				data1=self.conn.recv(4096)
				if (data1==b'done'):
					break
			f.close()
			print('file closed')
			UMS_services.insertfile(int(userid),filename,filesize)
			print('Entry maded in databse')
			print(os.getcwd())
		messagebox.showinfo('Edit field','file recived')
		print('server all file sent')
		os.chdir("..")
		os.chdir("..")
		
	def send_file(self,conn):
		os.chdir('uploaded_files')
		self.conn.send(('Send username').encode('latin-1'))
		username=self.conn.recv(1024).decode('latin-1')
		print(username)
		os.chdir(username)
		self.conn.send(('Send no of files').encode('latin-1'))
		nof=self.conn.recv(1024).decode('latin-1')
		print('server'+nof)
		self.conn.send(('Send filename').encode('latin-1'))
		for file in range(int(nof)):
			filename=self.conn.recv(4096).decode('latin-1')
			print(filename)
			f=open(filename,'rb')
			print('server reading data')
			data=f.read(4096)
			while data:
				self.conn.send(data)
				print('sending data of file')
				data=f.read(4096)
			f.close()
			print('file closing data send')
			self.conn.send(b'done')
			print('server file closed')
		print('server all file send')
		os.chdir("..")
		os.chdir("..")
		
	def re_move_file(self,conn):
		os.chdir('uploaded_files')
		self.conn.send(('Send username').encode())
		username=self.conn.recv(1024).decode()
		print(username)
		os.chdir(username)
		self.conn.send(('Send userid').encode())
		userid=self.conn.recv(1024).decode()
		print(userid)
		self.conn.send(('Send no. of files').encode())
		l=self.conn.recv(1024).decode()
		for  i in range(int(l)):
			x=self.conn.recv(4096).decode()
			os.remove(x)
			print(x)
			if (UMS_services.deletefile(x,int(userid))):
				messagebox.showinfo('Edit field','file deleted succesfully')
			else:
				messagebox.showerror('Edit field','unable to delete file.')
		print('All files deleted server side')	
		os.chdir("..")
		os.chdir("..")
	
	def re_name_file(self,conn):
		os.chdir('uploaded_files')
		self.conn.send(('Send username').encode())
		username=self.conn.recv(1024).decode()
		os.chdir(username)
		self.conn.send(('Send userid').encode())
		userid=self.conn.recv(1024).decode()
		self.conn.send(('Send the length of selelction').encode())
		l=self.conn.recv(1024).decode()
		for i in range(int(l)):
			self.conn.send(('Send old filename').encode())
			oldfname=self.conn.recv(4096).decode()
			self.conn.send(('Send new file name').encode())
			nfilename=self.conn.recv(4096).decode()
			os.rename(oldfname,nfilename)
			if (UMS_services.change_file_name(nfilename,userid,oldfname)):
				messagebox.showinfo('Edit field','file renamed succesfully')
			else:
				messagebox.showinfo('Edit field','unable to rename file')
		print('server file renamed succcess')
		os.chdir("..")
		os.chdir("..")
		
	def run(self):
		while True:
			u=self.conn.recv(1024).decode("latin-1")
			#self.conn.send(('Send username').encode('latin-1'))
			
			if (u=='Download'):
				self.send_file(self.conn)
			elif (u=='upload'):
				self.recv_file(self.conn)
			elif (u=='Remove'):
				self.re_move_file(self.conn)
			elif (u=='Rename'):
				self.re_name_file(self.conn)
		

class manage_profile:
	
	def __init__(self,userid,usertype):
		self.userid=userid
		self.usertype=usertype
		self.user=UMS_services.search(userid)
		self.editflag='view'
		self.root=tk.Tk()
		self.root.title('manage profile')
		self.root.geometry('500x400')
		
		tk.Label(self.root,text='USERID').grid(row=0,column=0,padx=10,pady=10)
		tk.Label(self.root,text='USER NAME').grid(row=1,column=0,padx=10,pady=10)
		tk.Label(self.root,text='NAME').grid(row=2,column=0,padx=10,pady=10)
		tk.Label(self.root,text='CONTACT').grid(row=3,column=0,padx=10,pady=10)
		tk.Label(self.root,text='ADDRESS').grid(row=4,column=0,padx=10,pady=10)
		tk.Label(self.root,text='GENDER').grid(row=5,column=0,padx=10,pady=10)
		tk.Label(self.root,text='EMAIL').grid(row=6,column=0,padx=10,pady=10)
		
		self.e=tk.Button(self.root,text='Edit',width=15,command=self.clk_edit)
		self.e.grid(row=7,column=0,padx=10,pady=10)
		self.s=tk.Button(self.root,text='Save',width=15,command=self.clk_save)
		self.s.grid(row=7,column=1,padx=10,pady=10)
		self.c=tk.Button(self.root,text='Cancel',width=15,command=self.clk_cancel)
		self.c.grid(row=7,column=2,padx=10,pady=10)
		
		self.gender=tk.StringVar()
		self.gender.set('0')
		self.ugm=tk.Radiobutton(self.root,text='Male',variable=self.gender,value='0')
		self.ugm.grid(row=5,column=1,padx=10,pady=10)
		self.ugf=tk.Radiobutton(self.root,text='Female',variable=self.gender,value='1')
		self.ugf.grid(row=5,column=2,padx=10,pady=10)
		
		self.uid=tk.Entry(self.root)
		self.uid.grid(row=0,column=1)
		self.uname=tk.Entry(self.root)
		self.uname.grid(row=1,column=1)
		self.name=tk.Entry(self.root)
		self.name.grid(row=2,column=1)
		self.ucontact=tk.Entry(self.root)
		self.ucontact.grid(row=3,column=1)
		self.uemail=tk.Entry(self.root)
		self.uemail.grid(row=6,column=1)
		self.uaddress=tk.Text(self.root,height=4,width=15)
		self.uaddress.grid(row=4,column=1)
	
		self.showRecord()
		self.s.config(state='disabled')
		self.root.mainloop()
	
	def enableAll(self):
		self.uid.config(state='normal')
		self.uname.config(state='normal')
		self.name.config(state='normal')
		self.ucontact.config(state='normal')
		self.uemail.config(state='normal')
		self.uaddress.config(state='normal')
		self.ugm.config(state='normal')
		self.ugf.config(state='normal')
	
	def disableAll(self):	
		self.uid.config(state='disabled')
		self.uname.config(state='disabled')
		self.name.config(state='disabled')
		self.ucontact.config(state='disabled')
		self.uemail.config(state='disabled')
		self.uaddress.config(state='disabled')
		self.ugm.config(state='disabled')
		self.ugf.config(state='disabled')
	
	def showRecord(self):
		self.enableAll()
		self.uid.delete(0,'end')
		self.uid.insert(0,int(self.user.getUserId()))
		self.uname.delete(0,'end')
		self.uname.insert(0,self.user.getUserName())
		self.name.delete(0,'end')
		self.name.insert(0,self.user.getName())
		self.ucontact.delete(0,'end')
		self.ucontact.insert(0,self.user.getContact())
		self.uemail.delete(0,'end')
		self.uemail.insert(0,self.user.getEmail())
		self.uaddress.delete(1.0,'end')
		self.uaddress.insert(1.0,self.user.getAddress())
		if (self.user.getGender()==0):
			self.gender.set('0')
		else:
			self.gender.set('1')
		self.disableAll()
	
	def clk_edit(self):
		self.e.config(state='disabled')
		self.s.config(state='normal')
		self.enableAll()
		self.uid.config(state='disabled')
		self.uname.config(state='disabled')
		self.editflag='edit'
		
	def clk_save(self):
		user1=User()
		user1.setContact(self.ucontact.get())
		user1.setEmail(self.uemail.get())
		user1.setAddress(self.uaddress.get(1.0,'end'))
		user1.setGender(int(self.gender.get()))
		user1.setName(self.name.get())
		if (UMS_services.updateProfile(user1,self.userid)):
			messagebox.showinfo('Edit field','Details updated sucessfully')
		else:
			messagebox.showerror('Edit field','Uanble to update')
		self.e.config(state='normal')
		self.editflag='view'
		self.s.config(state='disabled')
		self.user=UMS_services.search(self.userid)
		self.showRecord()
		
		
	def clk_cancel(self):
		if (self.editflag=='view'):
			self.root.destroy()
			B(self.userid,self.usertype)

		else:
			self.editflag='view'
			self.e.config(state='normal')
			self.s.config(state='disabled')
			self.showRecord()

class manage_user:
	
	def __init__(self,userid,usertype):
		self.userid=userid
		self.usertype=usertype
		self.root=tk.Tk()
		self.root.title('Manage user')
		self.root.geometry('600x500')
		
		
		tk.Label(self.root,text='USERID').grid(row=0,column=0,padx=10,pady=10)
		tk.Label(self.root,text='USER NAME').grid(row=1,column=0,padx=10,pady=10)
		tk.Label(self.root,text='USER TYPE').grid(row=2,column=0,padx=10,pady=10)
		tk.Label(self.root,text='USER STATUS').grid(row=3,column=0,padx=10,pady=10)
		tk.Label(self.root,text='NAME').grid(row=4,column=0,padx=10,pady=10)
		tk.Label(self.root,text='CONTACT').grid(row=5,column=0,padx=10,pady=10)
		tk.Label(self.root,text='ADDRESS').grid(row=6,column=0,padx=10,pady=10)
		tk.Label(self.root,text='EMAIL').grid(row=7,column=0,padx=10,pady=10)
		tk.Label(self.root,text='GENDER').grid(row=8,column=0,padx=10,pady=10)
		
		self.uid=tk.Entry(self.root)
		self.uid.grid(row=0,column=1)
		self.uname=tk.Entry(self.root)
		self.uname.grid(row=1,column=1)
		self.name=tk.Entry(self.root)
		self.name.grid(row=4,column=1)
		self.ucontact=tk.Entry(self.root)
		self.ucontact.grid(row=5,column=1)
		self.uemail=tk.Entry(self.root)
		self.uemail.grid(row=7,column=1)
		self.uaddress=tk.Text(self.root,height=4,width=15)
		self.uaddress.grid(row=6,column=1)
		
		self.gender=tk.StringVar()
		self.gender.set('0')
		self.ugm=tk.Radiobutton(self.root,text='Male',variable=self.gender,value='0')
		self.ugm.grid(row=8,column=1)
		self.ugf=tk.Radiobutton(self.root,text='Female',variable=self.gender,value='1')
		self.ugf.grid(row=8,column=2)
		
		self.status=tk.StringVar()
		self.status.set('0')
		self.usa=tk.Radiobutton(self.root,text='Active',variable=self.status,value='0')
		self.usa.grid(row=3,column=1)
		self.usi=tk.Radiobutton(self.root,text='Inactive',variable=self.status,value='1')
		self.usi.grid(row=3,column=2)
		
		self.type=tk.StringVar()
		self.type.set('Admin')
		self.utype=tk.OptionMenu(self.root,self.type,'Admin','User')
		self.utype.grid(row=2,column=1)
		
		self.f=tk.Button(self.root,text='First',width=15,command=self.clk_first)
		self.f.grid(row=9,column=0,padx=10,pady=10)
		self.p=tk.Button(self.root,text='Previous',width=15,command=self.clk_previous)
		self.p.grid(row=9,column=1,padx=10,pady=10)
		self.n=tk.Button(self.root,text='Next',width=15,command=self.clk_next)
		self.n.grid(row=9,column=2,padx=10,pady=10)
		self.l=tk.Button(self.root,text='Last',width=15,command=self.clk_last)
		self.l.grid(row=9,column=3,padx=10,pady=10)
		self.a=tk.Button(self.root,text='Add',width=15,command=self.clk_add)
		self.a.grid(row=10,column=0,padx=10,pady=10)
		self.e=tk.Button(self.root,text='Edit',width=15,command=self.clk_edit)
		self.e.grid(row=10,column=1,padx=10,pady=10)
		self.s=tk.Button(self.root,text='Save',width=15,command=self.clk_save)
		self.s.grid(row=10,column=2,padx=10,pady=10)
		self.c=tk.Button(self.root,text='Cancel',width=15,command=self.clk_cancel)
		self.c.grid(row=10,column=3,padx=10,pady=10)
		
		self.userlist=UMS_services.view()
		self.curr_index=0
		self.addeditflag='view'
		self.s.config(state='disabled')
		self.showRecord()	
		self.root.mainloop()
		
	def enableAll(self):
		self.uid.config(state='normal')
		self.uname.config(state='normal')
		self.name.config(state='normal')
		self.ucontact.config(state='normal')
		self.uemail.config(state='normal')
		self.uaddress.config(state='normal')
		self.ugm.config(state='normal')
		self.ugf.config(state='normal')
		self.usa.config(state='normal')
		self.usi.config(state='normal')
		self.utype.config(state='normal')
	
	def disableAll(self):
		self.uid.config(state='disabled')
		self.uname.config(state='disabled')
		self.name.config(state='disabled')
		self.ucontact.config(state='disabled')
		self.uemail.config(state='disabled')
		self.uaddress.config(state='disabled')
		self.ugm.config(state='disabled')
		self.ugf.config(state='disabled')
		self.usa.config(state='disabled')
		self.usi.config(state='disabled')
		self.utype.config(state='disabled')
		
	def showRecord(self):
		self.enableAll()
		user=self.userlist[self.curr_index]
		self.uid.delete(0,'end')
		self.uid.insert(0,str(user.getUserId()))
		self.uname.delete(0,'end')
		self.uname.insert(0,user.getUserName())
		self.name.delete(0,'end')
		self.name.insert(0,user.getName())
		self.ucontact.delete(0,'end')
		self.ucontact.insert(0,user.getContact())
		self.uemail.delete(0,'end')
		self.uemail.insert(0,user.getEmail())
		self.uaddress.delete(1.0,'end')
		self.uaddress.insert(1.0,user.getAddress())
		if (user.getUserStatus()==0):
			self.status.set('0')
		else:
			self.status.set('1')
		if (user.getGender()==0):
			self.gender.set('0')
		else:
			self.gender.set('1')
		
		if (user.getUserType()=='Admin'):
			self.type.set('Admin')
		else:
			self.type.set('User')
		self.disableAll()
		
		self.f.config(state='normal')
		self.n.config(state='normal')
		self.p.config(state='normal')
		self.l.config(state='normal')
		self.a.config(state='normal')
		
		if (self.curr_index==0):
			self.f.config(state='disabled')
			self.p.config(state='disabled')
		if (self.curr_index==len(self.userlist)-1):
			self.l.config(state='disabled')
			self.n.config(state='disabled')
	
	def clk_add(self):
		self.enableAll()
		self.addeditflag='add'
		self.s.config(state='normal')
		self.uid.delete(0,'end')
		self.uid.config(state='disabled')
		self.uname.delete(0,'end')
		self.name.delete(0,'end')
		self.ucontact.delete(0,'end')
		self.uaddress.delete(1.0,'end')
		self.uemail.delete(0,'end')
		self.gender.set('Male')
		self.status.set('Active')
		self.type.set('Admin')
		self.f.config(state='disabled')
		self.n.config(state='disabled')
		self.p.config(state='disabled')
		self.l.config(state='disabled')
		self.e.config(state='disabled')
		self.a.config(state='disabled')
		
	def clk_edit(self):
		self.enableAll()
		self.uid.config(state='disabled')
		self.uname.config(state='disabled')
		self.addeditflag='edit'
		self.s.config(state='normal')
		self.a.config(state='disabled')
		self.f.config(state='disabled')
		self.p.config(state='disabled')
		self.n.config(state='disabled')
		self.l.config(state='disabled')
		
	def clk_first(self):
		self.curr_index=0
		self.showRecord()
	
	def clk_next(self):
		self.curr_index+=1
		self.showRecord()
	
	def clk_previous(self):
		self.curr_index-=1
		self.showRecord()
	
	def clk_last(self):
		self.curr_index=(len(self.userlist)-1)
		self.showRecord()
	
	def clk_save(self):
		user=User()
		user.setUserType(self.type.get())
		user.setUserStatus(int(self.status.get()))
		user.setName(self.name.get())
		user.setEmail(self.uemail.get())
		user.setContact(self.ucontact.get())
		user.setAddress(self.uaddress.get(1.0,'end'))
		user.setGender(int(self.gender.get()))
		if (self.addeditflag=='add'):
			user.setUserName(self.uname.get())
			user.setPassword('anamika')
			if (UMS_services.add(user)):
				messagebox.showinfo('create new user','Added successfully with password anamika')
			else:
				messagebox.showerror('create new user','Unable to add.')
		elif (self.addeditflag=='edit'):
			self.uid.config(state='normal')
			user.setUserId(int(self.uid.get()))
			self.uid.config(state='disabled')
			if (UMS_services.update(user)):
				messagebox.showinfo('update','Updated Sucessfully')
			else:
				messagebox.showerror('update','Unable to update')
		self.s.config(state='disabled')
		self.a.config(state='normal')
		self.e.config(state='normal')
		self.userlist=UMS_services.view()
		if (self.addeditflag=='add'):
			self.curr_index=len(self.userlist)-1
		self.addeditflag='view'
		self.showRecord()
		
	def clk_cancel(self):
		if (self.addeditflag=='view'):
			self.root.destroy()
			B(self.userid,self.usertype)
		else:
			self.addeditflag='view'
			self.s.config(state='disabled')
			self.showRecord()
		
class Change_password:
	def __init__(self,w):
		self.userid=w
		self.root=tk.Tk()
		self.root.title('change password')
		self.root.geometry('500x200')
		tk.Label(self.root,text='Enter old password').grid(row=0,column=0,padx=10,pady=10)
		tk.Label(self.root,text='Enter new password').grid(row=1,column=0,padx=10,pady=10)
		self.oldPasswrd=tk.Entry(self.root)
		self.oldPasswrd.grid(row=0,column=1)
		self.newPasswrd=tk.Entry(self.root,show='*')
		self.newPasswrd.grid(row=1,column=1)
		tk.Button(self.root,text='change password',command=self.change).grid(row=2,column=0,padx=10,pady=10)
		tk.Button(self.root,text='clear',command=self.clear).grid(row=2,column=1,padx=10,pady=10)
		self.root.mainloop()
	def change(self):
		if Authentication.change_password(self.userid,self.oldPasswrd.get(),self.newPasswrd.get()):
			messagebox.showinfo('change password','Password changed sucessfully.')
			self.root.destroy()
			A()
		else:
			messagebox.showerror('change password','Password not changed.')
	def clear(self):
		self.oldPasswrd.delete(0,'end')
		self.newPasswrd.delete(0,'end')
			
		
		
		