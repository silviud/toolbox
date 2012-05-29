#!/usr/bin/python
"""
blurb: Very simple custom class import and usage example.
"""
from myclass import daSql
list = []
while True:
   a = daSql("mysql://hostname/dbname",username="myusername",password="mypassword")
   a.connect()
   list.append(a)
