from time import localtime, strftime
from ast import literal_eval
from subprocess import call
import sys


def runLouvain_PR(dirL, graphL, weigthsL, treeL, commL, netName, partName):
#    print "conv"
    cmd = dirL+"convert -i "+netName+" -o "+graphL+" -w "+weigthsL
    call([cmd],shell=True)
#    print "louvain"
    cmd = dirL+"louvain "+graphL+" -l -1 -q 0 -w "+weigthsL+" -p "+partName+" > "+treeL
    call([cmd],shell=True)
#    print "hierarchy"
    cmd = dirL+"hierarchy "+treeL
    call([cmd],shell=True)
#    print "hierarchy l 1"
    cmd = dirL+"hierarchy "+treeL+" -l 1 > "+commL
    call([cmd],shell=True)
    cmd = "rm "+graphL+" "+weigthsL+" "+treeL
    call([cmd],shell=True)



if len(sys.argv)!=3:
    print "\nUsage: "+sys.argv[0]+" <network> <threshold for recursion>"
    quit()

network_name = sys.argv[1]
size_threhold_for_recursion = literal_eval(sys.argv[2])



dir_data = "../data/subchallenge2/"
dir_louvain = "./louvain/"



#################################
#                               #
#   Loading the input network   #
#                               #
#################################


print strftime("%H:%M:%S", localtime())+": Loading the input network"

inFile = open(dir_data+network_name+".txt",'r')
neighbours = dict()
weights = dict()

for line in inFile:
    temp_array = line.rstrip().split("\t")
    node1 = temp_array[0]
    node2 = temp_array[1]
    weight = literal_eval(temp_array[2])

    if node1 not in neighbours:
        neighbours[node1] = []
    neighbours[node1].append(node2)
    weights[node1+"-"+node2] = weight

    # Assuming the graph is undirected
    if node2 not in neighbours:
        neighbours[node2] = []
    neighbours[node2].append(node1)
    weights[node2+"-"+node1] = weight


print strftime("%H:%M:%S", localtime())+": Loading the PageRank results"
    
PageRank = dict()
inFile = open("./PR_sc2_"+network_name+".txt",'r')
lines = inFile.readlines()
inFile.close()
for i in range(1,len(lines)):
    temp_array = lines[i].rstrip().split("\t")
    node = temp_array[0]
    PR = literal_eval(temp_array[5])
    PageRank[node] = PR


print strftime("%H:%M:%S", localtime())+": Generating initial partition"

outFile = open(dir_louvain+"partition_"+network_name+".txt",'w')
for n in neighbours:
    max_PR = PageRank[n]
    max_node = n
    for node in neighbours[n]:
        if PageRank[node] > max_PR:
            max_PR = PageRank[node]
            max_node = node
    outFile.write(n+" "+max_node+"\n")
outFile.close()




#################################
#                               #
#   Running 1st Louvain step    #
#                               #
#################################


print strftime("%H:%M:%S", localtime())+": Running Louvain"

graph_louvain = dir_louvain+network_name+"_graph.bin"
weigths_louvain = dir_louvain+network_name+"_graph.weights"
tree_louvain = dir_louvain+network_name+"_graph.tree"
comm_louvain = dir_louvain+network_name+"_graph_node2comm_level1"
part_louvain = dir_louvain+"partition_"+network_name+".txt"

runLouvain_PR(dir_louvain, graph_louvain, weigths_louvain, tree_louvain, comm_louvain, dir_data+network_name+".txt", part_louvain)




#################################
#                               #
#    Processing the results     #
#                               #
#################################


print strftime("%H:%M:%S", localtime())+": Loading the communities"

inFile = open(comm_louvain,'r')
communities = dict()
communities_needing_recursion = []

for line in inFile:
    temp_array = line.rstrip().split(" ")
    node = temp_array[0]
    community = temp_array[1]
    if community not in communities:
        communities[community] = []
    communities[community].append(node)

inFile.close()


print strftime("%H:%M:%S", localtime())+": ("+str(len(communities))+" communities)"

print strftime("%H:%M:%S", localtime())+": Processing"

comm_louvain_analysis = dir_louvain+network_name+"_allValidCommunities.txt"

outFile = open(comm_louvain_analysis,'w')
#outFile.write("Community ID\tSize\tConnectivity\tWeighted connectivity\n")

nb_main_comm = 0
nb_invalid_comm = 0

for comm in communities:
    connectivity = 0.0 # pretty much the clustering coefficient of that community
    weighted_connectivity = 0.0 # the weighted version
    if len(communities[comm]) > size_threhold_for_recursion:
        communities_needing_recursion.append(communities[comm])
    elif len(communities[comm])>2:
        nb_main_comm+=1
        txt = ""
        for node1 in communities[comm]:
            txt += node1+"\t"
            for node2 in communities[comm]:
                if node1 in neighbours[node2]:
                    connectivity+=1
                    weighted_connectivity+=weights[node1+"-"+node2]
        connectivity = connectivity/(len(communities[comm])*(len(communities[comm])-1))
        weighted_connectivity = weighted_connectivity/(len(communities[comm])*(len(communities[comm])-1))
        outFile.write("m"+str(nb_main_comm)+"\t"+str(weighted_connectivity)+"\t"+txt.rstrip()+"\n")
    else:
        nb_invalid_comm+=1

print strftime("%H:%M:%S", localtime())+": "+str(nb_main_comm)+" communities extracted, "+str(len(communities_needing_recursion))+" sent to recursion"




#################################
#                               #
#   Recursion on communities    #
#                               #
#################################

print strftime("%H:%M:%S", localtime())+": Recursion"

i=0
while i<len(communities_needing_recursion):
    comm = str(i+1)
    print strftime("%H:%M:%S", localtime())+":\tSubcommunity "+comm+"/"+str(len(communities_needing_recursion))+" ("+str(len(communities_needing_recursion[i]))+" nodes)"

    # Extract the subnetwork that corresponds to this community
    print strftime("%H:%M:%S", localtime())+":\t\tSubnetwork extraction"
    
    subnetwork = dir_louvain+network_name+"_subnetwork_community_"+comm+".txt"
    outFileSN = open(subnetwork,'w')
    inFile = open(dir_data+network_name+".txt",'r')
    for line in inFile:
        temp_array = line.rstrip().split("\t")
        node1 = temp_array[0]
        node2 = temp_array[1]
        if node1 in communities_needing_recursion[i] and node2 in communities_needing_recursion[i]:
            outFileSN.write(line)
    inFile.close()
    outFileSN.close()

    # Extract the PageRank data for this subnetwork
    print strftime("%H:%M:%S", localtime())+":\t\tLoading the PageRank results"

    PageRankSN = dict()
    inFile = open("./PR_sc2_"+network_name+".txt",'r')
    lines = inFile.readlines()
    inFile.close()
    for l in range(1,len(lines)):
        temp_array = lines[l].rstrip().split("\t")
        node = temp_array[0]
        PR = literal_eval(temp_array[5])
        if node in communities_needing_recursion[i]:
            PageRankSN[node] = PR


    print strftime("%H:%M:%S", localtime())+":\t\tGenerating initial partition"

    part_louvain = dir_louvain+"partition_"+network_name+"_"+comm+".txt"
    outFileSN = open(part_louvain,'w')
    for n in communities_needing_recursion[i]:
        max_PR = PageRankSN[n]
        max_node = n
        for node in neighbours[n]:
            if node in communities_needing_recursion[i]:
                if PageRankSN[node] > max_PR:
                    max_PR = PageRankSN[node]
                    max_node = node
        outFileSN.write(n+" "+max_node+"\n")
    outFileSN.close()


    # Run Louvain on this subnetwork
    print strftime("%H:%M:%S", localtime())+":\t\tRunning Louvain"

    graph_louvain = dir_louvain+network_name+"_subnetwork_community_"+comm+"_graph.bin"
    weigths_louvain = dir_louvain+network_name+"_subnetwork_community_"+comm+"_graph.weights"
    tree_louvain = dir_louvain+network_name+"_subnetwork_community_"+comm+"_graph.tree"
    comm_louvain = dir_louvain+network_name+"_subnetwork_community_"+comm+"_graph_node2comm_level1"
    
    runLouvain_PR(dir_louvain, graph_louvain, weigths_louvain, tree_louvain, comm_louvain, subnetwork, part_louvain)



    # Analyse the results
    print strftime("%H:%M:%S", localtime())+":\t\tProcessing the results"

    inFile = open(comm_louvain,'r')
    subcommunities = dict()

    for line in inFile:
        temp_array = line.rstrip().split(" ")
        node = temp_array[0]
        community = temp_array[1]
        if community not in subcommunities:
            subcommunities[community] = []
        subcommunities[community].append(node)

    inFile.close()

    comm_louvain_analysis = dir_louvain+network_name+"_analysis_subcommunities_"+comm+".txt"

#    outFile = open(comm_louvain_analysis,'w')
#        outFile.write("Subcommunity ID\tSize\tConnectivity\tWeighted connectivity\n")

    nb_subcomm = 0
    nb_added_for_recursion = 0

    for subcomm in subcommunities:
        if len(subcommunities[subcomm]) > size_threhold_for_recursion:
            # we only send subcommunities for recursion, there would be no point processing the same community again
            if len(subcommunities[subcomm]) < len(communities_needing_recursion[i]):
                nb_added_for_recursion+=1
                communities_needing_recursion.append(subcommunities[subcomm])
        elif len(subcommunities[subcomm])>2:
            nb_subcomm+=1
            txt = ""
            connectivity = 0.0 # pretty much the clustering coefficient of that community
            weighted_connectivity = 0.0 # the weighted version
            for node1 in subcommunities[subcomm]:
                txt += node1+"\t"
                for node2 in subcommunities[subcomm]:
                    if node1 in neighbours[node2]:
                        connectivity+=1
                        weighted_connectivity+=weights[node1+"-"+node2]
            connectivity = connectivity/(len(subcommunities[subcomm])*(len(subcommunities[subcomm])-1))
            weighted_connectivity = weighted_connectivity/(len(subcommunities[subcomm])*(len(subcommunities[subcomm])-1))
            outFile.write("s"+str(i+1)+"\t"+str(weighted_connectivity)+"\t"+txt.rstrip()+"\n")
        else:
            nb_invalid_comm+=1

#    outFile.close()
    print strftime("%H:%M:%S", localtime())+":\t\t"+str(nb_subcomm)+" subcommunities extracted, "+str(nb_added_for_recursion)+" sent to recursion"

    if nb_subcomm+nb_invalid_comm+nb_added_for_recursion==1:
        print strftime("%H:%M:%S", localtime())+": Done. (safety break)"
        outFile.close()
        quit()


#    cmd = "rm "+subnetwork+" "+graph_louvain+" "+weigths_louvain+" "+tree_louvain
#    call([cmd],shell=True)

    i+=1

outFile.close()

print strftime("%H:%M:%S", localtime())+": Done."
