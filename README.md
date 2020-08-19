# FTP Server 
+--------------+
* FTP stands for File Transfer Protocol, this project provides the feature to transfer files between server and client.
* It is based upon 3-tier based architecture.
* It implements the concept of socket Programming.
* The project has two sections: 
  * 1. Server
  * 2. Client
* Server is the program that provides the feature to the client to transfer files to server.
* Clinet in the simple words is user who can use the facility of transfering files provided by the server.
* At a particular instance of time, multiple clients can get connected to server.
* This provides also has the User Management System which is devloped with the vision to manage profile of users in an organisation.

# The 3 pillars of Project
-----------------------------
    * Presentaion Layer: The Presentaion Layer is the top layer, communicates with the Buisness Layer and Data Layer and provides 
                         the smooth acess to the clients.
            * The Presentaion Layer has two files:
              1. Login.py : Login code implementaion for the clients.
              2. main_frame.py : GUI Functions implementations for the clients.
    * Buisness Layer : The Business Layer is the intermediate layer, act as bridge between Presentation Layer and Data Layer.
            * The Buisness Layer has two files:
              1. login_services.py : This file implements the code for authenticating client in database.
              2. UMS_services.py   : This file implements the code for managing users in database.
    * Data Layer : This Layer is the core and holds the entire data for the program.
            * The Data Layer has two files:
              1. DBConnection.py   : Establishes connection with database.
              2. User.py           : It fetchs the record for each particular user.


              
