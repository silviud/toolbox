#!/usr/bin/python

"""
runall.py by Kegan Holtzhausen

This can run a command as a user with a password or with certificate on remote machines. Also supports uploading of file/script

REQUIRES pexepct
yum install pexpect
or
apt-get install pexpect
"""

import pexpect
import getpass, os
import sys
import getopt

def debugMsg(msg):
    if verbose == True:
        print "DEBUG: " + str(msg)

def usage():
    print 'runall.py'
    print 'by Kegan Holtzhausen'
    print
    print 'Uses python expect to login and execute commands on remote machines. Also supports uploading of script and certificate authentication'
    print
    print 'mandatory options:'
    print ' -h|--host= hosts list eg: "mltapp21 mltapp22 mltapp23"'
    print ' -u|--user= user eg: "gf3"'
    print ' -c|--command= command in quotes to execute eg: "~/install.sh -all --my -options"'
    print
    print 'optional options:'
    print ' -f|--file= file to upload eg: "~/install.sh"'
    print
    print 'Examples:'
    print './runall.py -h "mltapp25 mltapp26 mltapp27 mltapp28" -u gf3 -c "~/install.sh" -f install.sh'
    print './runall.py -h "mltapp25 mltapp26 mltapp27 mltapp28" -u gf3 -c "~/gsf-trunk/util/bin/svnglassfish-config.sh autobuild trunk"'
    print './runall.py -h mltapp21 -u gf3 -c ". ~/.bash_profile && ~/gsf-trunk/util/bin/install_domain.sh walletapi2domain"'
    print './runall.py -h "kwkapp19 kwkapp20"  -u gf3 -c "crontab < ~/gsf-trunk/util/etc/crontab"'

def ssh_command (user, host, password, command):
    """This runs a command on the remote host.
auto accepts fingerprint and continue connecting. """
    ssh_newkey = 'Are you sure you want to continue connecting'
    prompt = '$'
    child = pexpect.spawn('ssh -l %s %s %s'%(user, host, command), timeout=120)
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: ', prompt])
    print "matched :" + str(i)
    if i == 0: # Timeout
        print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None
    if i == 1: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        child.expect ('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0: # Timeout
            print 'ERROR!'
            print 'SSH could not login. Here is what SSH said:'
            print child.before, child.after
            return None
        if i == 1: # password
            child.sendline(password)
    if i == 2:
        print "2 matched, I think that means send ass word"
        child.sendline(password)
    if i == 3:
        print "2 matched, I think that means we have prompt"
    return child

def scp_command (user, host, password, file):
    """ SCP a file up to home dir of user logging in as """
    print "scp_command"
    ssh_newkey = 'Are you sure you want to continue connecting'
    prompt = '$'
    print "child"
    child = pexpect.spawn('scp %s %s@%s:'%(file, user, host))
    print " i ="
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: ', prompt])
    print "matched :" + str(i)
    if i == 0: # Timeout
        print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None
    if i == 1: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        child.expect ('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0: # Timeout
            print 'ERROR!'
            print 'SCP could not login. Here is what SCP said:'
            print child.before, child.after
            return None       
        print "2 matched, I think that means send ass word"
        child.sendline(password)
    if i == 3:
        print "2 matched, I think that means we have prompt"
    return child



def main ():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:f:h:u:", ["command=", "file=", "host=", "user="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            hosts = arg
            debugMsg('setting host to ' + arg)
        elif opt in ("-u", "--user"):
            user = arg
            debugMsg('setting user to ' + arg)
        elif opt in ("-f", "--file"):
            file = arg
            debugMsg('setting domain to ' + arg)
        elif opt in ("-c", "--command"):
            command = arg
            debugMsg('setting command to ' + arg)
        else:
            print 'skipping INVALID opt: ' + opt + ' ' + arg

    errors = ""
    try:
        file
    except:
        file = ""
    #hosts = raw_input('Hostname(s) space separated: ')
    #user = raw_input('Username: ')
    password = getpass.getpass('Password for user ' + user + ': ')
    #file = raw_input('File to Upload to HOME if any?: ')
    #command = raw_input('Command ( full paths ): ')

    for host in hosts.split(" "):
        try:
            if file != "":
                print "SCP to " + host
                child1 = scp_command (user, host, password, file)
                child1.expect(pexpect.EOF)
                print child1.before
            if command != "":
                print "SSH to " + host + " and execute " + command
                child = ssh_command (user, host, password, command)
                child.expect(pexpect.EOF)
                print child.before
        except Exception, e:
            print "Error with HOST: " + str(host)
            print str(e)
            errors = errors + ", " + host
	print "Where were errors with " + errors

if __name__ == '__main__':
    try:
        if len(sys.argv) < 4:
            usage()
        else:
            verbose=True
            main()
    except Exception, e:
        print str(e)
        os._exit(1)

