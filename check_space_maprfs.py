#!/usr/bin/python

import sys, getopt, os, subprocess, re
from subprocess import Popen, PIPE

maprcli = "/opt/mapr/bin/maprcli"
gmetric = "/usr/bin/gmetric"
hadoop = "/usr/bin/hadoop"

def options():
   grep = "none"
   try:
      opts, args = getopt.getopt(sys.argv[1:], "d:h", ["help", "grep="])
   except getopt.GetoptError as err:
      print(err)
      usage()
      sys.exit(2)
   for opt, args in opts:
      if opt in ("-h"):
	 usage()
         sys.exit()
      elif opt in ("-d"):
         return args

def excutablecheck(command): # checks if the file is excutable
	if os.access(command, os.F_OK):
		return
	else: 
		sys.exit

def usage():
	 print 'usage:'
      	 print 'check_space_mapr.py -h '
         print 'check_space_mapr.py -d <directory name>'
	
if __name__ == "__main__":
	directory = options()


''' Check if the commands are excutable '''
excutablecheck(hadoop)
excutablecheck(gmetric)

''' Set up the full hadoop command '''
hadoop+=" fs -dus "
hadoop+= directory

''' grab the maprcli output '''
p = subprocess.Popen(hadoop, shell=True, stdout=PIPE, bufsize=1)
aggregation = 0
for line in p.stdout.readlines():
	searchObj = re.search('maprfs', line, flags=0)
	if searchObj:
		line.strip()	
		dir,number = line.split()
		aggregation = int(number)
		'''  convert to GB '''
		aggregation = aggregation/1024/1024/1024

directory = directory.replace('/','.')
directory = directory[1:-1]
print aggregation, directory
cmd = gmetric
cmd += " --name "
cmd += directory
cmd += " --value "
aggregation = str(aggregation)
cmd += aggregation
cmd += " --type=int16 --units=Gigabytes --group=volume_metrics"
print cmd
o = subprocess.Popen(cmd, shell=True, stdout=PIPE, bufsize=1)
o.stdout.close()
o.wait()	

p.stdout.close()
p.wait()
