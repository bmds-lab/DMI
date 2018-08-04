

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

python convertToUndirected.py
python normaliseWeights.py 3_signal_anonym_undirected_v3
python normaliseWeights.py 6_homology_anonym_v2


########################
# Calculating PageRank #
#  on all six networks #
########################

# Note: this needs to run only once

# Usage: ./pageRank <nb_nodes> <nb_edges> <input_file> <output_file> <directed|undirected>

# Network 1

 ./pageRank 17397 2232405 ../data/subchallenge1/1_ppi_anonym_v2.txt ./PR_1_ppi_anonym_v2.txt undirected

# Network 2

./pageRank 12420 397309 ../data/subchallenge1/2_ppi_anonym_v2.txt ./PR_2_ppi_anonym_v2.txt undirected

# Network 3

./pageRank 5254 21826 ../data/subchallenge1/3_signal_anonym_undirected_v3_normalised.txt ./PR_3_signal_anonym_undirected_v3_normalised.txt undirected

# Network 4

 ./pageRank 12588 1000000 ../data/subchallenge1/4_coexpr_anonym_v2.txt ./PR_4_coexpr_anonym_v2.txt undirected

# Network 5

./pageRank 14679 1000000 ../data/subchallenge1/5_cancer_anonym_v2.txt ./PR_5_cancer_anonym_v2.txt undirected

# Network 6

./pageRank 10475 4223606 ../data/subchallenge1/6_homology_anonym_v2_normalised.txt ./PR_6_homology_anonym_v2_normalised.txt undirected


########################
# Running our method   #
#  on the six networks #
########################

# Usage: python enhancedRecursiveLouvain_recPR_sc1.py <network> <threshold for recursion>

python enhancedRecursiveLouvain_recPR_sc1.py 1_ppi_anonym_v2 80 
python enhancedRecursiveLouvain_recPR_sc1.py 2_ppi_anonym_v2 80 
python enhancedRecursiveLouvain_recPR_sc1.py 3_signal_anonym_undirected_v3_normalised 80 
python enhancedRecursiveLouvain_recPR_sc1.py 4_coexpr_anonym_v2 95 
python enhancedRecursiveLouvain_recPR_sc1.py 5_cancer_anonym_v2 90 
python enhancedRecursiveLouvain_recPR_sc1.py 6_homology_anonym_v2_normalised 80

python finaliseEnhancedLouvain_sc1.py 

