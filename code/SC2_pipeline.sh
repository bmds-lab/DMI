

#######################
# Assumed structure   #
#  and required files #
#######################

# Two folders, "data" and "code"

# The "data" folder contains two folders, "subchallenge1" and "subchallenge2", which contain the input networks

# The "code" folder contains our code, as well as a folder "louvain" which contains the executable files "convert", "matrix", "louvain" and "hierarchy", which are all compiled from the file "louvain-generic.tar.gz" downloaded from http://sourceforge.net/projects/louvain/

# File pageRank.c needs to be compiled to an executable called "pageRank" (in the "code" folder)

# The following commands assume that "code" is the working directory


######################
# Pre-processing for #
#  networks 3 and 6  #
######################

# Note: this needs to run only once

python convertToUndirected_sc2.py
python normaliseWeights_sc2.py 3_signal_anonym_aligned_undirected_v3
python normaliseWeights_sc2.py 6_homology_anonym_aligned_v2


########################
# Calculating PageRank #
#  on all six networks #
########################

# Note: this needs to run only once

# Usage: ./pageRank <nb_nodes> <nb_edges> <input_file> <output_file> <directed|undirected>

# Network 1

./pageRank 21115 2232405 ../data/subchallenge2/1_ppi_anonym_aligned_v2.txt ./PR_sc2_1_ppi_anonym_aligned_v2.txt undirected

# Network 2

./pageRank 21115 397309 ../data/subchallenge2/2_ppi_anonym_aligned_v2.txt ./PR_sc2_2_ppi_anonym_aligned_v2.txt undirected

# Network 3

./pageRank 21115 21826 ../data/subchallenge2/3_signal_anonym_aligned_undirected_v3_normalised.txt ./PR_sc2_3_signal_anonym_aligned_undirected_v3_normalised.txt undirected

# Network 4

./pageRank 21115 1000000 ../data/subchallenge2/4_coexpr_anonym_aligned_v2.txt ./PR_sc2_4_coexpr_anonym_aligned_v2.txt undirected

# Network 5

./pageRank 21115 1000000 ../data/subchallenge2/5_cancer_anonym_aligned_v2.txt ./PR_sc2_5_cancer_anonym_aligned_v2.txt undirected

# Network 6

./pageRank 21115 4223606 ../data/subchallenge2/6_homology_anonym_aligned_v2_normalised.txt ./PR_sc2_6_homology_anonym_aligned_v2_normalised.txt undirected



########################
# Running our method   #
#  on the six networks #
########################

# Usage: python enhancedRecursiveLouvain_recPR_sc2.py <network> <threshold for recursion>

python enhancedRecursiveLouvain_recPR_sc2.py 1_ppi_anonym_aligned_v2 80
python enhancedRecursiveLouvain_recPR_sc2.py 2_ppi_anonym_aligned_v2 80 
python enhancedRecursiveLouvain_recPR_sc2.py 3_signal_anonym_aligned_undirected_v3_normalised 80 
python enhancedRecursiveLouvain_recPR_sc2.py 4_coexpr_anonym_aligned_v2 95 
python enhancedRecursiveLouvain_recPR_sc2.py 5_cancer_anonym_aligned_v2 90 
python enhancedRecursiveLouvain_recPR_sc2.py 6_homology_anonym_aligned_v2_normalised 80

python finaliseEnhancedLouvain_sc2.py 


###############
# Voting step #
###############

# Usage: java -Xmx4g -jar CogeneMatrix.jar <file1> <file2> ... <file6>
# where fileX is the path to network X

java -Xmx4g -jar CogeneMatrix.jar ./louvain/1_ppi_anonym_aligned_v2.txt ./louvain/2_ppi_anonym_aligned_v2.txt ./louvain/3_signal_anonym_aligned_undirected_v3_normalised.txt ./louvain/4_coexpr_anonym_aligned_v2.txt ./louvain/5_cancer_anonym_aligned_v2.txt ./louvain/6_homology_anonym_aligned_v2_normalised.txt 


#########################
# Running our method    #
#  on the vote networks #
#########################

# Usage: python enhancedRecursiveLouvain_recPR_sc2.py <network> <threshold for recursion>

python enhancedRecursiveLouvain_recPR_sc2.py communities_graph_uniform_voting 80
python enhancedRecursiveLouvain_recPR_sc2.py communities_graph_weighted_voting 80

python finaliseEnhancedLouvain_step2_sc2.py 

