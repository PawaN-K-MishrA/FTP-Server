import tkinter as tk
from tkinter import messagebox
import main_frame
import sys
sys.path.append('..')
from buissness.login_services import Authentication
class A:
	def __init__(self):
		self.root=tk.Tk()
		self.root.geometry('300x150')
		self.root.title('login')
		tk.Label(self.root,text='Username').grid(row=0,column=0)
		tk.Label(self.root,text='Password').grid(row=1,column=0)
		self.v1=tk.Entry(self.root)
		self.v1.grid(row=0,column=1)
		self.v2=tk.Entry(self.root,show='*')
		self.v2.grid(row=1,column=1)
		tk.Button(self.root,text='login',command=self.login_click).grid(row=2,column=1)
		tk.Button(self.root,text='clear',command=self.clear).grid(row=2,column=0)
		#tk.Button(self.frame,text='change password',command=self.change_passwd).grid(row=2,column=2)
		#self.v2.bind("<Return>",self.login_click)

		self.root.mainloop()
	def clear(self):
		self.v1.delete(0,'end')
		self.v2.delete(0,'end')
	
	def login_click(self):
		w=Authentication.loginCheck(self.v1.get(),self.v2.get())
		un=self.v1.get()
		if (w != -1):
			if (self.v2.get()=='anamika'):
				self.root.destroy()
				main_frame.Change_password(w,un)
				
			else:
				self.root.destroy()
				main_frame.B(w,un)
				
		else:
			messagebox.showerror('LOGIN',"Username and password didn't match")
if __name__=='__main__':
	A()	
	