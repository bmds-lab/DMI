from ast import literal_eval

in_ = "../data/subchallenge2/3_signal_anonym_aligned_directed_v3.txt"
out_ = "../data/subchallenge2/3_signal_anonym_aligned_undirected_v3.txt"

inFile = open(in_,'r')
min = 9999
max = 0

edges = dict()

for line in inFile:
    temp_array = line.rstrip().split("\t")
    node1 = literal_eval(temp_array[0])
    node2 = literal_eval(temp_array[1])
    weight = literal_eval(temp_array[2])
    edges[str(node1)+"-"+str(node2)] = weight
    if node1 > max:
        max = node1
    if node1 < min:
        min = node1
    if node2 > max:
        max = node2
    if node2 < min:
        min = node2

inFile.close()

outFile = open(out_,'w')

for i in range(min,max):
    for j in range(i+1,max+1):
        weight = 0.0
        edge1 = str(i)+"-"+str(j)
        edge2 = str(j)+"-"+str(i)
        if edge1 in edges:
            weight+=edges[edge1]
        if edge2 in edges:
            weight+=edges[edge2]
        if weight>0:
            outFile.write(str(i)+"\t"+str(j)+"\t"+str(weight/2)+"\n")

outFile.close()


