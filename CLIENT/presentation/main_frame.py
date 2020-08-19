import sys
import os
sys.path.append('..')
import tkinter as tk
from tkinter import ttk
from login import A
from tkinter import messagebox
from tkinter import filedialog
from buissness.login_services import Authentication
from buissness.UMS_services import UMS_services
from data.user import User
import socket
import time
class B:
	def __init__(self,w,un):
		self.userid=w
		self.username=un
		self.root=tk.Tk()
		self.s=socket.socket()
		self.s.connect(('localhost',12345))
		self.root.title('FTP Server'+' '+'welcome'+' '+str(self.username))
		self.root.geometry('500x400')
		
		self.menubar=tk.Menu(self.root)
		self.logoutmenu=tk.Menu(self.menubar,tearoff=0)
		self.logoutmenu.add_command(label='logout',command=self.out)
		self.logoutmenu.add_command(label='change password',command=self.back1)
		self.menubar.add_cascade(label='logout',menu=self.logoutmenu)
		self.umsmenu=tk.Menu(self.menubar,tearoff=0)
		#self.umsmenu.add_command(label='manage user',command=self.back2)
		self.umsmenu.add_command(label='manage profile',command=self.back3)
		self.menubar.add_cascade(label='UMS',menu=self.umsmenu)
		self.ftpmenu=tk.Menu(self.menubar,tearoff=0)
		self.ftpmenu.add_command(label='Upload',command=self.back4)
		self.ftpmenu.add_command(label='Download',command=self.back5)
		self.menubar.add_cascade(label='FILE MANAGER',menu=self.ftpmenu)
		self.root.config(menu=self.menubar)
		self.root.mainloop()
	
	def out(self):
		Authentication.logout()
		A()
	
	def back1(self):
		self.root.destroy()
		Change_password(self.userid,self.username)
	
	def back2(self):
		self.root.destroy()
		manage_user(self.userid)
	
	def back3(self):
		self.root.destroy()
		manage_profile(self.userid,self.username)
	
	def back4(self):
		
		Upload_file(self.userid,self.username,self.s)
	
	def back5(self):
		
		Download_file(self.userid,self.username,self.s)

class Download_file:
	def __init__(self,userid,username,s):
		self.userid=userid
		self.username=username
		self.s=s
		self.root=tk.Tk()
		self.root.title('Download a file')
		self.root.geometry('900x400')
		
		lfile=UMS_services.viewfilesbyid(self.userid)
		self.treeview=ttk.Treeview(self.root,column=('col1','col2'),show='headings',selectmode='extended')
		self.treeview.place(x=0,y=0,width=600,height=300)
		self.treeview.heading('#1',text='File Name')
		self.treeview.heading('#2',text='Size')
		#print(lfile)
		for i in lfile:
			self.treeview.insert('','end',i[0],values=i)
		self.vsb = ttk.Scrollbar(self.treeview, orient="vertical", command=self.treeview.yview)
		self.vsb.pack(side='right', fill='y')
		self.treeview.configure(yscrollcommand=self.vsb.set)
		
		self.dd=tk.Button(self.root,text='Download',width=15,command=self.recv_file)
		self.dd.place(x=700,y=10)
		self.rm=tk.Button(self.root,text='Remove',width=15,command=self.re_move)
		self.rm.place(x=700,y=40)
		self.rn=tk.Button(self.root,text='Rename',width=15,command=self.re_name)
		self.rn.place(x=700,y=70)
		self.treeview.bind('<<TreeviewSelect>>',self.callback)
		self.root.mainloop()
	
	def callback(self,root):
		l=[]
		sel_one=self.treeview.selection()
		for fn in sel_one:
			l.append(fn)
		return l
				
	
	def recv_file(self):
		l=self.callback(self.root)
		print(l)
		self.s.send(('Download').encode('latin-1'))
		self.s.recv(1024).decode('latin-1')
		self.s.send((self.username).encode('latin-1'))
		self.s.recv(1024).decode('latin-1')
		self.s.send((str(len(l))).encode('latin-1'))
		self.s.recv(1024).decode()
		for i in l:
			self.s.send((i).encode('latin-1'))
			print(i+ ' client fileopened')
			f=open(i,'wb')
			print('client reciving data')
			data1=self.s.recv(4096)
			while data1:
				f.write(data1)
				print('writing in file')
				data1=self.s.recv(4096)
				if (data1==b'done'):
					print('file closing data recived current file closed')
					break
			f.close()
			print('client file closed')
		messagebox.showinfo('Edit field','file downloading complete')
		
	
	def re_move(self):
		self.s.send(('Remove').encode())
		x1=self.s.recv(1024).decode()
		self.s.send((self.username).encode())
		l=self.callback(self.root)
		x2=self.s.recv(1024).decode()
		self.s.send(str(self.userid).encode())
		x3=self.s.recv(1024).decode()
		self.s.send(str(len(l)).encode())
		print(l)
		for i in l:
			print(i)
			self.s.send((i).encode())
			#if (UMS_services.deletefile(i,self.userid)):
				#messagebox.showinfo('Edit field','file deleted succesfully')
			#else:
				#messagebox.showerror('Edit field','unable to delete file.')
		print('all file sent')
		self.root.destroy()
	def re_name(self):
		self.namechange=tk.Entry(self.root)
		self.namechange.place(x=700,y=100)
		
		self.OK=tk.Button(self.root,text='OK',width=15,command=self.renameouter)
		self.OK.place(x=750,y=130)
		
	
	def rename(self,userid,username):
		self.new_file_name=self.namechange.get()
		self.s.send(('Rename').encode())
		x1=self.s.recv(1024).decode()
		self.s.send((username).encode())
		x2=self.s.recv(1024).decode()
		self.s.send(str(userid).encode())
		l=self.callback(self.root)
		x3=self.s.recv(1024).decode()
		self.s.send(str(len(l)).encode())
		print(self.new_file_name)
		for i in l:
			x4=self.s.recv(1024).decode()
			self.s.send((i).encode())
			x5=self.s.recv(1024).decode()
			self.s.send((self.new_file_name).encode())
		print('client all file sent')
		self.root.destroy()
		
	def renameouter(self):
		self.rename(self.userid,self.username)
			
		
		
		
		 
class Upload_file:
	def __init__(self,userid,username,s):
		self.userid=userid
		self.username=username
		self.s=s
		self.root=tk.Tk()
		self.root.title('upload a file')
		self.root.geometry('300x150')
		self.sf=tk.Button(self.root,text='select file',width=15,command=self.openpath)
		self.sf.grid(row=0,column=0,padx=10,pady=10)
		self.gp=tk.Entry(self.root)
		self.gp.grid(row=0,column=1)
		self.ud=tk.Button(self.root,text='Upload',width=15,command=self.send_file)
		self.ud.grid(row=1,column=1)
		self.root.mainloop()
	def openpath(self):
		self.name=filedialog.askopenfilenames()
		self.u=self.root.tk.splitlist(self.name)
		self.gp.insert(0,self.u)
		
	
	def send_file(self):
		self.s.send('upload'.encode('latin-1'))
		self.s.recv(1024).decode('latin-1')
		self.s.send((self.username).encode('latin-1'))
		self.s.recv(1024).decode('latin-1')
		self.s.send(str((self.userid)).encode('latin-1'))
		self.s.recv(1024).decode('latin-1')
		nof=len(self.u)
		print('client'+str(nof))
		
		self.s.send(str(nof).encode('latin-1'))
		self.s.recv(1024).decode('latin-1')
		print(self.u)
		for i in self.u:
			filesize=os.path.getsize(i)
			print(filesize)
			k=0
			while (filesize>=1024):
				filesize=filesize/1024
				k+=1
			if (k==1):
				filesize=str(filesize)+'Kb'
			elif (k==2):
				filesize=str(filesize)+'Mb'
			elif (k==3):
				filesize=str(filesize)+'Gb'
			x=(i.split('/'))
			filename=x[-1]
			print(filesize)
			
			self.s.send((filesize).encode('latin-1'))
			self.s.recv(1024).decode('latin-1')
			self.s.send((filename).encode('latin-1'))
			print(filename)
			self.s.recv(1024).decode('latin-1')
			print("filename ack sent")
			f=open(i,'rb')
			print("file opened")
			data=f.read(4096)
			while (data):
				self.s.send(data)
				#print('client sending file')
				data=f.read(4096)
				print("reading data")
			f.close()
			print('file closed')
			self.s.send(b'done')
		print('client all file sent')
		self.root.destroy()
		
		
	
	
		
		

class manage_profile:
	
	def __init__(self,userid,username):
		self.userid=userid
		self.username=username
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
			B(self.userid,self.username)

		else:
			self.editflag='view'
			self.e.config(state='normal')
			self.s.config(state='disabled')
			self.showRecord()
			
class manage_user:
	
	def __init__(self,userid):
		self.userid=userid
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
			B(self.userid)
		else:
			self.addeditflag='view'
			self.s.config(state='disabled')
			self.showRecord()
			
class Change_password:
	def __init__(self,w,un):
		self.username=un
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
			
		
		
		