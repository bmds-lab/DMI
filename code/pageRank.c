#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>



/**************************************/
/**         printTimestamp()         **/
/**************************************/

/*
 Prints a custom string with the current time and a given message
 Input: the message we want to include
 Output: none
 */

int printTimestamp(char* infoString) {
    time_t rawtime;
    struct tm * timeinfo;
    char buffer1 [15];
    char buffer2 [80];
    
    time (&rawtime);
    timeinfo = localtime (&rawtime);
    strftime (buffer1,80,"%H:%M:%S ->\t",timeinfo);
    
    strcpy(buffer2, buffer1);
    strcat(buffer2, infoString);
    puts (buffer2);
    
    return 0;
}





/**************************************/
/**            pageRank()            **/
/**************************************/

/*
 Calculates page
 Input: number of nodes, number of edges, adjacency matrix, PR array, outdegree array
 Output: PR values
 */

int pageRank(int nb_nodes, int nb_edges, double** adj, double* rank_v1, double* rank_v2, double* rank_v3, double* rank_v4, int* degree) {
    
    double tmp_v1, tmp_v2, tmp_v3, tmp_v4, d=0.85;
    int iterMax=100;
    
    for(int iter=0; iter<iterMax; ++iter) {
        /*printf("Iter %02d:\t0 - %lf\t1 - %lf\t3 - %lf\t3 - %lf\t4 - %lf\n",iter,rank_v1[0],rank_v1[1],rank_v1[2],rank_v1[3],rank_v1[4]);*/
        for(int i=0; i<nb_nodes; ++i) {
            tmp_v1 = 0;
            tmp_v2 = 0;
            tmp_v3 = 0;
            tmp_v4 = 0;
            for(int j=0; j<nb_nodes; ++j) {
                if(adj[j][i]>0) {
                    tmp_v1 += rank_v1[j]/degree[j];
                    tmp_v2 += rank_v2[j]/degree[j];
                    tmp_v3 += adj[j][i]*rank_v3[j]/degree[j];
                    tmp_v4 += adj[j][i]*rank_v4[j]/degree[j];
                }
            }
            rank_v1[i] = (1-d)/nb_nodes + d*tmp_v1; /* normal one, with sum of ranks equal to 1 */
            rank_v2[i] = (1-d) + d*tmp_v2; /* normal one but without dividing by the number of nodes */
            rank_v3[i] = (1-d) + d*tmp_v3; /* with weights */
            rank_v4[i] = (1-d)/nb_nodes + d*tmp_v4; /* with weights */
        }
    }
    return 0;
}





/**************************************/
/**              main()              **/
/**************************************/

/*
 Reads the input data
 Input: number of nodes, number of edges, input file
 Output: none
 */

int main(int argc, char* argv[]) {
    
    if(argc!=6) {
        printf("Usage: ./pageRank <nb_nodes> <nb_edges> <input_file> <output_file> <directed|undirected>\n");
        return 1;
    }
    
    /* Parameters */
    int nb_nodes = atoi(argv[1]);
    int nb_edges = atoi(argv[2]);
    char *inname = argv[3], *outname = argv[4], *type = argv[5];
    
    /* Variables */
    FILE *infile, *outfile;
    char line[100];
    int i = 0, node1, node2, inDeg, outDeg, *inDegree, *outDegree;
    double edge_weight;
    double **adj, *rank_v1, *rank_v2, *rank_v3, *rank_v4;
    
    /* Memory allocation: adjacency matrix, degree array, rank array */
    /* Note: quick and dirty approach; we might consider better data structures later */
    adj = (double**)malloc(sizeof(double*)*nb_nodes);
    inDegree = (int*)malloc(sizeof(int)*nb_nodes);
    outDegree = (int*)malloc(sizeof(int)*nb_nodes);
    rank_v1 = (double*)malloc(sizeof(double)*nb_nodes);
    rank_v2 = (double*)malloc(sizeof(double)*nb_nodes);
    rank_v3 = (double*)malloc(sizeof(double)*nb_nodes);
    rank_v4 = (double*)malloc(sizeof(double)*nb_nodes);
    for(int n=0; n<nb_nodes; ++n) {
        adj[n] = (double*)malloc(sizeof(double)*nb_nodes);
        inDegree[n] = 0;
        outDegree[n] = 0;
        rank_v1[n] = 1;
        rank_v2[n] = 1;
        rank_v3[n] = 1;
        rank_v4[n] = 1;
        for(int m=0; m<nb_nodes; ++m) {
            adj[n][m] = 0;
        }
    }
    
    
    printTimestamp("Reading the input file");
    
    /* Opening the input file */
    infile = fopen(inname, "r");
    if (!infile) {
        printf("Couldn't open %s for reading\n", inname);
        return 2;
    }
    
    /* Reading each line */
    while(fgets(line, sizeof(line), infile) != NULL) {
        sscanf(line, "%d\t%d\t%lf", &node1, &node2, &edge_weight);
        adj[node1][node2] = edge_weight;
        if(strcmp(type,"undirected")==0)
            adj[node2][node1] = edge_weight;
    }

    printTimestamp("Degree");

    /* Calculating indegrees and outdegrees */
    for(int n=0; n<nb_nodes; ++n) {
        outDeg = 0;
        inDeg = 0;
        for(int m=0; m<nb_nodes; ++m) {
            if(adj[n][m]>0)
                ++outDeg;
            if(adj[m][n]>0)
                ++inDeg;
        }
        inDegree[n] = inDeg;
        outDegree[n] = outDeg;
    }
    
    printTimestamp("PageRank");

    /* Calculating pageRank */
    pageRank(nb_nodes,nb_edges,adj,rank_v1,rank_v2,rank_v3,rank_v4,outDegree);

    
    printTimestamp("Saving");
    
    /* Opening the output file */
    outfile = fopen(outname, "w");
    if (!outfile) {
        printf("Couldn't open %s for writing\n", outname);
        return 3;
    }

    double total = 0;
    for(int n=0; n<nb_nodes; ++n)
        total += rank_v3[n];
    
    
    fprintf(outfile,"Node\tIn\tOut\tRank_1\tRank_2\tRank_3\n");
    for(int n=0; n<nb_nodes; ++n) {
        fprintf(outfile,"%d\t%d\t%d\t%lf\t%lf\t%lf\t%lf\n",n,inDegree[n],outDegree[n],rank_v1[n],rank_v2[n],rank_v3[n],rank_v4[n]);
    }

    printTimestamp("Done.");
    return 0;
}
