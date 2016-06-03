import os
import sys
import periodic_search_crude

size = int(sys.argv[1])

for i in xrange(size**2):
    if i % size == 0:
        sys.stdout.write("\n")
    period = periodic_search_crude.main(str(i))
    if period == 0:
        sys.stdout.write("-")
    elif period < 4:
        sys.stdout.write("0")
    elif period < 8:
        sys.stdout.write("1")
    elif period < 12:
        sys.stdout.write("2")
    elif period < 16:
        sys.stdout.write("3")
    elif period < 20:
        sys.stdout.write("4")
    elif period < 24:
        sys.stdout.write("5")
    elif period < 28:
        sys.stdout.write("6")
    elif period < 32:
        sys.stdout.write("7")
    elif period < 36:
        sys.stdout.write("8")
    else:
        sys.stdout.write("9")
    #sys.stdout.write(str(periodic_search_crude.main(str(i))))
    os.chdir("..")
print ""
