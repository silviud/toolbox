#!/usr/bin/python
from myclass import daSql
list = []
while True:
   a = daSql("mysql://hostname/dbname",username="myusername",password="mypassword")
   a.connect()
   list.append(a)
