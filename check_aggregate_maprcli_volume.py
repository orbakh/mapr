#!/usr/bin/python

import sys, getopt, os, subprocess, re
from subprocess import Popen, PIPE

maprcli = "/opt/mapr/bin/maprcli"
gmetric = "/usr/bin/gmetric"


def excutablecheck(command): 
 if os.access(command, os.F_OK):
  return
 else: 
  sys.exit


excutablecheck(maprcli)
excutablecheck(gmetric)

maprcli+=" volume list -columns \"mountdir,logicalUsed,used\""

p = subprocess.Popen(maprcli, shell=True, stdout=PIPE, bufsize=1)
aggregate_total_used = 0 
aggregate_total_logical = 0 
aggregate_pe_used = 0 
aggregate_pe_logical = 0 
aggregate_meld_used = 0 
aggregate_meld_logical = 0 
aggregate_meld_sem_used = 0 
aggregate_meld_sem_logical = 0 
aggregate_meld_int_used = 0 
aggregate_meld_int_logical = 0 
aggregate_meld_meta_used = 0 
aggregate_meld_meta_logical = 0 
aggregate_meld_src_used = 0 
aggregate_meld_src_logical = 0 
aggregate_meld_src_x1_used = 0 
aggregate_meld_src_x1_logical = 0 
aggregate_meld_src_bali_used = 0 
aggregate_meld_src_bali_logical = 0 
aggregate_meld_src_merlin_used = 0 
aggregate_meld_src_merlin_logical = 0 
aggregate_meld_src_overlay_used = 0 
aggregate_meld_src_overlay_logical = 0 
aggregate_meld_base_used = 0 
aggregate_meld_base_logical = 0 
aggregate_meld_base_x1_used = 0 
aggregate_meld_base_x1_logical = 0 
aggregate_meld_base_bali_used = 0 
aggregate_meld_base_bali_logical = 0 
aggregate_meld_base_cemp_used = 0
aggregate_meld_base_cemp_logical  = 0
aggregate_meld_base_merlin_used = 0 
aggregate_meld_base_merlin_logical = 0 
aggregate_meld_base_overlay_used = 0 
aggregate_meld_base_overlay_logical = 0 
aggregate_user_used = 0 
aggregate_user_logical= 0 
aggregate_mapr_used = 0 
aggregate_mapr_logical= 0 
aggregate_ebi_used = 0 
aggregate_ebi_logical= 0 
for line in p.stdout.readlines():
 line.strip() 
 parts = line.split()
 if len(parts) <= 2:
  continue
 directory,logical,used = line.split()
 if directory == 'mountdir':
  continue
 logical = int(logical)
 used = int(used)
 aggregate_total_used +=  used
 aggregate_total_logical +=  logical
 if "pe" in directory:
  aggregate_pe_used +=  used
  aggregate_pe_logical +=  logical
 elif "mapr" in directory:
  aggregate_mapr_used +=  used
  aggregate_mapr_logical +=  logical
 elif "ebi" in directory:
  aggregate_ebi_used +=  used
  aggregate_ebi_logical +=  logical
 elif "aps" in directory:
  aggregate_meld_used +=  used
  aggregate_meld_logical +=  logical
  if "src" in directory:
   aggregate_meld_src_used += used
   aggregate_meld_src_logical += logical
   if "x1" in directory:
    aggregate_meld_src_x1_used += used 
    aggregate_meld_src_x1_logical += logical 
   elif "bali" in directory:
    aggregate_meld_src_bali_used += used 
    aggregate_meld_src_bali_logical += logical 
   elif "merlin" in directory:
    aggregate_meld_src_merlin_used += used 
    aggregate_meld_src_merlin_logical += logical 
   elif "overlay" in directory:
    aggregate_meld_src_overlay_used += used 
    aggregate_meld_src_overlay_logical += logical 
  if "base" in directory:
   aggregate_meld_base_used += used
   aggregate_meld_base_logical += logical
   if "x1" in directory:
    aggregate_meld_base_x1_used += used 
    aggregate_meld_base_x1_logical += logical 
   elif "bali" in directory:
    aggregate_meld_base_bali_used += used 
    aggregate_meld_base_bali_logical += logical 
   elif "cemp" in directory:
    aggregate_meld_base_cemp_used += used 
    aggregate_meld_base_cemp_logical += logical 
   elif "merlin" in directory:
    aggregate_meld_base_merlin_used += used 
    aggregate_meld_base_merlin_logical += logical 
   elif "overlay" in directory:
    aggregate_meld_base_overlay_used += used 
    aggregate_meld_base_overlay_logical += logical 
  if "sem" in directory:
   aggregate_meld_sem_used += used
   aggregate_meld_sem_logical += used
  if "int" in directory:
   aggregate_meld_int_used += used
   aggregate_meld_int_logical += used
  if "meta" in directory:
   aggregate_meld_meta_used += used
   aggregate_meld_meta_logical += used
 
 elif "user" in directory:
  aggregate_user_used +=  used
  aggregate_user_logical +=  logical

# print("directory = {0} logical used = {1} real used = {2}".format(directory,logical,used))

my_data = {'aggregate_pe_used': aggregate_pe_used}
my_data['aggregate_pe_logical'] = aggregate_pe_logical
my_data['aggregate_user_logical'] = aggregate_user_logical
my_data['aggregate_user_used'] = aggregate_user_used
my_data['aggregate_meld_logical'] = aggregate_meld_logical
my_data['aggregate_meld_used'] = aggregate_meld_used
my_data['aggregate_meld_base_logical'] = aggregate_meld_base_logical
my_data['aggregate_meld_base_used'] = aggregate_meld_base_used
my_data['aggregate_meld_base_bali_logical'] = aggregate_meld_base_bali_logical
my_data['aggregate_meld_base_bali_used'] = aggregate_meld_base_bali_used
my_data['aggregate_meld_base_x1_logical'] = aggregate_meld_base_x1_logical
my_data['aggregate_meld_base_x1_used'] = aggregate_meld_base_x1_used
my_data['aggregate_meld_base_cemp_logical'] = aggregate_meld_base_cemp_logical
my_data['aggregate_meld_base_cemp_used'] = aggregate_meld_base_cemp_used
my_data['aggregate_meld_base_merlin_logical'] = aggregate_meld_base_merlin_logical
my_data['aggregate_meld_base_merlin_used'] = aggregate_meld_base_merlin_used
my_data['aggregate_meld_base_overlay_logical'] = aggregate_meld_base_overlay_logical
my_data['aggregate_meld_base_overlay_used'] = aggregate_meld_base_overlay_used
my_data['aggregate_meld_src_logical'] = aggregate_meld_src_logical
my_data['aggregate_meld_src_used'] = aggregate_meld_src_used
my_data['aggregate_meld_src_bali_logical'] = aggregate_meld_src_bali_logical
my_data['aggregate_meld_src_bali_used'] = aggregate_meld_src_bali_used
my_data['aggregate_meld_src_x1_logical'] = aggregate_meld_src_x1_logical
my_data['aggregate_meld_src_x1_used'] = aggregate_meld_src_x1_used
my_data['aggregate_meld_src_merlin_logical'] = aggregate_meld_src_merlin_logical
my_data['aggregate_meld_src_merlin_used'] = aggregate_meld_src_merlin_used
my_data['aggregate_meld_src_overlay_logical'] = aggregate_meld_src_overlay_logical
my_data['aggregate_meld_src_overlay_used'] = aggregate_meld_src_overlay_used
my_data['aggregate_meld_sem_logical'] = aggregate_meld_sem_logical
my_data['aggregate_meld_sem_used'] = aggregate_meld_sem_used
my_data['aggregate_meld_int_logical'] = aggregate_meld_int_logical
my_data['aggregate_meld_int_used'] = aggregate_meld_int_used
my_data['aggregate_meld_meta_logical'] = aggregate_meld_meta_logical
my_data['aggregate_meld_meta_used'] = aggregate_meld_meta_used
my_data['aggregate_mapr_logical'] = aggregate_mapr_logical
my_data['aggregate_mapr_used'] = aggregate_mapr_used
my_data['aggregate_ebi_logical'] = aggregate_ebi_logical
my_data['aggregate_ebi_used'] = aggregate_ebi_used
my_data['aggregate_total_logical'] = aggregate_total_logical
my_data['aggregate_total_used'] = aggregate_total_used


for key in my_data:
	number = str(my_data[key])
#	print gmetric, "--name ", key, " --value ", number, " --type=int16 --units=Megabytes --group=maprcli_volume_metrics"
	cmd = gmetric
	cmd += " --name "
	cmd += key
	cmd += " --value "
	cmd += number
	cmd += " --type=int16 --units=Megabytes --group=maprcli_volume_metrics"
#	print cmd

	o = subprocess.Popen(cmd, shell=True, stdout=PIPE, bufsize=1)
	o.stdout.close()
	o.wait()


p.stdout.close()
p.wait()
