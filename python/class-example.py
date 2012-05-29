#!/usr/bin/python
from myclass import daSql
list = []
while True:
   a = daSql("somehost:3306",username="myusername",password="mypassword")
   a.connect()
   list.append(a)
