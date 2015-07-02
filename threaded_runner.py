import sys
import subprocess
import time

if len(sys.argv) < 3:
    print "Use: python threaded_runner file_list.txt cores"
    print "file_list.txt: The list of parameter files to be used in p21_sim"
    print "cores: The number of cores to be used at once."

files = open(sys.argv[1], 'r').readlines()
num_procs = int(sys.argv[2])

proclist = []
for i in xrange(num_procs):
    proclist.append(None)

cur_process = 0
last_started = 0

for f in files:
    while True:
        if proclist[cur_process] == None or proclist[cur_process].poll() != None:
            proclist[cur_process] = subprocess.Popen("python p21_sim.py " + f, shell="True")
            last_started = cur_process
            cur_process += 1
            cur_process = cur_process % num_procs
            break
        cur_process += 1
        cur_process = cur_process % num_procs
        if cur_process == last_started:
            time.sleep(1)
