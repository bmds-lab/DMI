from ast import literal_eval
import sys

if len(sys.argv)!=2:
    print "\nUsage: "+sys.argv[0]+" <network>"
    quit()

network_name = sys.argv[1]

dir_data = "../data/subchallenge2/"

in_name = network_name+".txt"
out_name = network_name+"_normalised.txt"

max = 0.0
edges = []

inFile = open(dir_data+in_name,'r')
for line in inFile:
    temp_array = line.rstrip().split("\t")
    weight = literal_eval(temp_array[2])
    if weight>max:
        max=weight
    edges.append(temp_array)
inFile.close()

if max>1:
    outFile = open(dir_data+out_name,'w')
    for i in range(0,len(edges)):
        outFile.write(edges[i][0]+"\t"+edges[i][1]+"\t"+str(literal_eval(edges[i][2])/max)+"\n")
    outFile.close()
    print "Normalised (maximum weight was "+str(max)+")"

else:
    print "Maximum weight is "+str(max)
