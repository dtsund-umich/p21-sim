import sys
import os

#Do 10x10 search for each pair of parameters.
size = 10

#Iterate over each pair of parameters.
parameter_list = open(sys.argv[1], 'r').readlines()
for i in xrange(len(parameter_list)-1):
    for j in xrange(i+1,len(parameter_list)):
        pairfile = open("pair.txt", 'w')
        pairfile.write(parameter_list[i] + parameter_list[j].strip())
        print "Across: " + parameter_list[i].split()[0] + " ranges from " + parameter_list[i].split()[1] + " to " + parameter_list[i].split()[2]
        print "Down: " + parameter_list[j].split()[0] + " ranges from " + parameter_list[j].split()[1] + " to " + parameter_list[j].split()[2]
        pairfile.close()
        
        #Generate the parameter space and solve the equations.
        os.system("python latin_hypercube.py pair.txt " + str(size) + " pair -e -s")
        os.system("python threaded_runner.py pair_list.txt 8")
        
        os.system("python figure.py " + str(size))
        
        #Cleanup.
        os.system("rm *pair*txt")
        os.system("rm -r */")
        print ""
        print ""
        print ""
