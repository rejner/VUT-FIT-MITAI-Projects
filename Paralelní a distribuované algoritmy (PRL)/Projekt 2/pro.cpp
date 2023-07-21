/*
*  PRL Project 2 - Implementation of order assignment to preorder vertices with Open MPI
*  Author:  Michal Rein (xreinm00)
*  File:    pro.c
*  Date:    22.04.2022
*/

#include <mpi.h>
#include <math.h>
#include <vector>

#define MASTER 0
#define END -1

#define forward_edge  (!(rank % 2))

using namespace std;

/* 
*  Structure representing oriented edge.
*  Each edge contains indices of their source and destination node. 
*/
struct edge {
    unsigned from_index;
    unsigned to_index;
    edge(unsigned from, unsigned to) : from_index(from), to_index(to) {};
};

/*
*   Implemented as defined at the lecture.
*   @param reversal_edge_rank  Rank of the edge reversive to current edge.
*   @param adjacency_list      Adjacency list.
*   @return Etour(e) value i.e. successor of current processor (edge).
*/
int adjacency_next(int reversal_edge_rank, vector<int> adjacency_list) {
    int len = adjacency_list.size();
    for (int i = 0; i < len; i++) {
        if (i % 2 == 0 && adjacency_list.at(i) == reversal_edge_rank) {
            return (len > i + 2) ? adjacency_list.at(i+2) : adjacency_list.at(0);
        }
    }
    return -1; // should not happen
}

/****************************
*           MAIN
****************************/
int main(int argc, char** argv) {

    int rank;
    int size;
    
    if (argc < 2) {
        cerr << "Not enough parameters!\n";
        return 1;
    } 

    // Binary tree as array, left_child_index = (2*i), right_child_index = (2*i) + 1 
    string tree_vertices = argv[1];
    int vertices_num = tree_vertices.length();

    //MPI INIT
    MPI_Init(&argc,&argv);           
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Create seperate communicator for processes responsible for forward edges only
    MPI_Comm FORWARD_COMM;
    int forward = forward_edge;     // tag if process will be responsible for forward edge
    int forward_rank, forward_size;
    // Split WORLD communicator
    MPI_Comm_split(MPI_COMM_WORLD, forward, rank, &FORWARD_COMM);
    MPI_Comm_rank(FORWARD_COMM, &forward_rank);
    MPI_Comm_size(FORWARD_COMM, &forward_size);

    // Assign edges to processors.
    // Each even processor (0, 2, 4...) is responsible for forward edge (deeper into the tree)
    // Each odd processor  (1, 3, 5...) is responsible for reversal edge
    // Since each process represents one edge lexicographically ordered, dividing rank by 4
    // returns index of source node (each full node has 4 edges total), children can be indexed
    // in a similar way (2 edges to each child). 
    edge *my_edge;
    forward_edge ? my_edge = new edge(floor(rank/4),   floor(rank/2)+1) :
                   my_edge = new edge(floor(rank/2)+1, floor(rank/4));

    vector<int> adjacency_list; // format: [e_1, e_1r, e_2, e_2r, e_3, e_3r]

    // PREORDER: ROOT -> LEFT -> RIGHT

    // parent edges (excluding root)
    if (my_edge->to_index != 0) {
        adjacency_list.push_back(2*(my_edge->to_index - 1) + 1); // reversal
        adjacency_list.push_back(2*(my_edge->to_index - 1));
    }

    // destination node should have left child, include connecting edges into adjacency_list
    if (2*(my_edge->to_index + 1) <= tree_vertices.length()) { 
        adjacency_list.push_back(4*(my_edge->to_index));
        adjacency_list.push_back(4*(my_edge->to_index) + 1);
    }

    // destination node should have right child, include connecting edges into adjacency_list
    if (2*(my_edge->to_index + 1) + 1 <= tree_vertices.length()) { 
        adjacency_list.push_back(4*(my_edge->to_index) + 2);
        adjacency_list.push_back(4*(my_edge->to_index) + 3);
    }

    // Calculate part of Euler's tour from adjacency list, i.e. successor of my edge
    int rank_of_inverted_edge = forward_edge ? rank + 1 : rank - 1;
    int successor = adjacency_next(rank_of_inverted_edge, adjacency_list);

    // Send rank to sucessor (every processes discovers it's predecessor)
    int predecessor;
    MPI_Send(&rank, 1, MPI_INT, successor, 0, MPI_COMM_WORLD);
    MPI_Recv(&predecessor, 1, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

    // Wait until all processes know their predecessors
    MPI_Barrier(MPI_COMM_WORLD);

    // Init value used for Suffix Sums (all forward edges weights sums)
    int weight = forward_edge ? 1 : 0;

    // Perform Suffix Sums between processes
    int msg[2];                                          // message buffer for transfering values
    successor   = successor == MASTER ? END : successor; // tag end of the cycle  (don't send anything to master)
    predecessor = rank == MASTER ? END : predecessor;    // tag end of the cycle  (master doesn't receive any)
    MPI_Status stat;
    
    for (int i = 0; i < log2(size); i++) {
        // save current predecessor
        int tmp_pre = predecessor; 
        // Send my predecessor rank to successor (successor will send values to my predecessor in the next round)
        // don't send anything to successor tagged as END (tour start, MASTER)
        if (successor != END) MPI_Send(&predecessor, 1, MPI_INT, successor, 0, MPI_COMM_WORLD);
            
        if (predecessor != END) {
            // Receive new predecessor rank
            MPI_Recv(&predecessor, 1, MPI_INT, tmp_pre, 0, MPI_COMM_WORLD, &stat);
            // Construct message to my current predecessor
            msg[0] = weight;
            msg[1] = successor;
            MPI_Send(&msg, 2, MPI_INT, tmp_pre, 0, MPI_COMM_WORLD);
        }

        if (successor != END) {
            // Receive message from successor, add weight value and set successor to my successor's successor
            MPI_Recv(&msg, 2, MPI_INT, successor, 0, MPI_COMM_WORLD, &stat);
            weight += msg[0];
            successor = msg[1];
        }
        // Wait for all processes to finish cycle
        MPI_Barrier(MPI_COMM_WORLD);
    }


    // result_indices will hold <position index>-<value index> pairs
    // All processes within FORWARD_COMM communicator will send their results to master
    int result_indices[vertices_num*2];
    if (forward_edge) {
        weight = vertices_num - weight; // weight correction
        msg[0] = weight;                // position
        msg[1] = my_edge->to_index;     // vertice index
        MPI_Gather(&msg, 2, MPI_INT, result_indices, 2, MPI_INT, MASTER, FORWARD_COMM);
    }
    
    // Master now should have information about vertices and their indices in the preorder ordered array.
    // Reconstruct the final array and print results.
    if (rank == MASTER) {
        char preorder[vertices_num];    // Array for vertices in the final order
        int final_index, node_index;    // index of the final placement within preorder array + vertice index

        // Construct final ordering from results
        preorder[0] = tree_vertices[0]; // root will always be the same
        for (int i = 0; i < (vertices_num-1)*2; i+=2) {
            final_index = result_indices[i];
            node_index = result_indices[i+1];
            preorder[final_index] = tree_vertices[node_index];
        }

        // Print final results
        for (int i = 0; i < vertices_num; i++) {
            cout << preorder[i];
        }
        cout << endl;
    }

    MPI_Finalize();
    return 0;
}