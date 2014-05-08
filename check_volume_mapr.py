#!/usr/bin/python

import sys, getopt, os, subprocess, re
from subprocess import Popen, PIPE

maprcli = "/opt/mapr/bin/maprcli"
gmetric = "/usr/bin/gmetric"

def options():
   grep = "none"
   try:
      opts, args = getopt.getopt(sys.argv[1:], "g:h", ["help", "grep="])
   except getopt.GetoptError as err:
      print(err)
      usage()
      sys.exit(2)
   for opt, args in opts:
      if opt in ("-h"):
	 usage()
         sys.exit()
      elif opt in ("-g"):
         return args

def excutablecheck(command): # checks if the file is excutable
	if os.access(command, os.F_OK):
		return
	else: 
		sys.exit

def usage():
	 print 'usage:'
      	 print 'check_space_mapr.py -h '
         print 'check_space_mapr.py -g <filesystem name>'
	
if __name__ == "__main__":
	grep = options()


''' Check if the commands are excutable '''
excutablecheck(maprcli)
excutablecheck(gmetric)

''' Set up the full maprcli command '''
maprcli+=" volume list -columns \"volumename,used\""

''' grab the maprcli output '''
p = subprocess.Popen(maprcli, shell=True, stdout=PIPE, bufsize=1)
aggregate = 0	
for line in p.stdout.readlines():
	searchObj = re.search(grep, line, flags=0)
	if searchObj:
		line.strip()	
		status = 0
		number,directory = line.split()
		number = int(number)
		aggregate += number
		number =  number/1024 
		if number > 1024:
			status = 1
			number = float(number)
			number = number/1024
		cmd = gmetric
		cmd += " --name "
		cmd += directory
		cmd += " --value "
		number = str(number)
		cmd += number
		if status == 0:
			cmd += " --type=int16 --units=Gigabytes --group=volume_metrics"
		else:
			cmd += " --type=int16 --units=Terabytes --group=volume_metrics"

		o = subprocess.Popen(cmd, shell=True, stdout=PIPE, bufsize=1)
		o.stdout.close()
	  	o.wait()
	  	
''' Do math to publish aggregate number in either GB or TB to gangila '''

aggregate = aggregate/1024
if number > 1024:
	aggregate = aggregate/1024
	aggregate = str(aggregate)
	cmd = gmetric
	cmd += " --name db."
	cmd += grep
	cmd += " --value "
	cmd += aggregate
	cmd += " --type=int16 --units=Terabytes --group=volume_metrics"
	o = subprocess.Popen(cmd, shell=True, stdout=PIPE, bufsize=1)
	o.stdout.close()
	o.wait()	
else:
	aggregate = str(aggregate)
	cmd = gmetric
	cmd += " --name db."
	cmd += grep
	cmd += " --value "
	cmd += aggregate
	cmd += " --type=int16 --units=Terabytes --group=volume_metrics"
	o = subprocess.Popen(cmd, shell=True, stdout=PIPE, bufsize=1)
	o.stdout.close()
	o.wait()	

p.stdout.close()
p.wait()
