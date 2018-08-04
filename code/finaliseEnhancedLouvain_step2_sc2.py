
dir = "./louvain/"


networks_in = ["communities_graph_uniform_voting_allValidCommunities.txt", "communities_graph_weighted_voting_allValidCommunities.txt"]

networks_out = ["communities_graph_uniform_voting.txt", "communities_graph_weighted_voting.txt"]

for i in range(0,len(networks_in)):
    inFile = open(dir+networks_in[i],'r')
    outFile = open(dir+networks_out[i],'w')
    j=1
    for line in inFile:
        ID = line.rstrip().split("\t")[0]
        outFile.write(str(j)+line[len(ID):])
        j+=1
    inFile.close()
    outFile.close()

