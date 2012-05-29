#!/usr/bin/python
"""
blurb: Simple LDAP connect and search example.
"""
import ldap

l = ldap.initialize('ldap://ldap.domain.com')
username = "cn=Directory Manager"
password = "mypasswordhere"

try:
	l.protocol_version = ldap.VERSION3
	l.simple_bind_s(username, password)
	valid = True
except Exception, error:
	print "Binding error"
	print error

baseDN = "ou=customers,ou=somedomain,ou=sites,dc=domain,dc=com"
searchScope = ldap.SCOPE_SUBTREE
retrieveAttributes = ["uid","forceMigration"]
searchFilter = "(&(uid=*)(jurisdiction=IT)(forceMigration=true))"

try:
	ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
	result_set = []
	while 1:
		result_type, result_data = l.result(ldap_result_id, 0)
		if (result_data == []):
			break
		else:
			print "Result: %s" % ( result_data )
			## here you don't have to append to a list
			## you could do whatever you want with the individual entry
			## The appending to list is just for illustration. 
			if result_type == ldap.RES_SEARCH_ENTRY:
				result_set.append(result_data)
	print result_set
except ldap.LDAPError, e:
	print e
