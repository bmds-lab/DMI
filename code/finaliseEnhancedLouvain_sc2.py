
dir = "./louvain/"


networks_in = ["1_ppi_anonym_aligned_v2_allValidCommunities.txt", "2_ppi_anonym_aligned_v2_allValidCommunities.txt", "3_signal_anonym_aligned_undirected_v3_normalised_allValidCommunities.txt", "4_coexpr_anonym_aligned_v2_allValidCommunities.txt", "5_cancer_anonym_aligned_v2_allValidCommunities.txt", "6_homology_anonym_aligned_v2_normalised_allValidCommunities.txt"]

networks_out = ["1_ppi_anonym_aligned_v2.txt", "2_ppi_anonym_aligned_v2.txt", "3_signal_anonym_aligned_undirected_v3_normalised.txt", "4_coexpr_anonym_aligned_v2.txt", "5_cancer_anonym_aligned_v2.txt", "6_homology_anonym_aligned_v2_normalised.txt"]

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

