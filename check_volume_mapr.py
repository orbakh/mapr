#!/usr/bin/python

import sys, getopt, os, subprocess, re
from subprocess import Popen, PIPE

maprcli = "/opt/mapr/bin/maprcli"
gmetric = "/usr/bin/gmetric"

def main(argv):
   grep = ''
   try:
      opts, args = getopt.getopt(argv,"g:",["grep="])
   except getopt.GetoptError:
      print 'check_space_mapr.py -g <filesystem name> '
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'check_space_mapr.py -g <filesystem name>'
         sys.exit()
      elif opt in ("-g", "--grep"):
         grep = arg

if __name__ == "__main__":
   main(sys.argv[1:])

def excutablecheck(command): # checks if the file is excutable
	if os.access(command, os.F_OK):
		return
	else: 
		sys.exit


''' Check if the commands are excutable '''
excutablecheck(maprcli)
excutablecheck(gmetric)

''' Set up the full maprcli command '''
maprcli+=" volume list -columns \"volumename,used\""

''' grab the maprcli output '''
p = subprocess.Popen(maprcli, shell=True, stdout=PIPE, bufsize=1)
for line in p.stdout.readlines():
	searchObj = re.search('aps', line, flags=0)
	if searchObj:
		line.strip()	
		status = 0
		number,directory = line.split()
		number = int(number)
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

p.stdout.close()
p.wait()

	
