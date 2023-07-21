/*
*  PRL Project 1 - Implementation of Odd-even merge sort with Open MPI
*  Author:  Michal Rein (xreinm00)
*  File:    oems.c
*  Date:    04.04.2022
*/

#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>

#define BUF_SIZE 8
#define MIN_TAG 1
#define MAX_TAG 2
#define MASTER 0

/*
*  Swap two elements in an array of size 2
*/
void swap_nums(unsigned char *buf) {
   unsigned char tmp = buf[0];
   buf[0] = buf[1];
   buf[1] = tmp;
}

/*
*  Logic of each computation element (CE) - except of the first layer input CEs
*  Each element has its computation cycl:
*     - Wait for incoming data from previous layer CEs
*     - Compare received values, sort them into *nums array ([0] -> MIN, [1] -> MAX)
*     - Send sorted values to other connected CEs
*/
void recv_process_send(int recv_min_rank, int recv_max_rank, int send_min_rank, int send_max_rank, unsigned char* nums) {
   MPI_Request req1, req2, req3, req4;
   MPI_Status stat1, stat2, stat3, stat4;
   // Receive data from previous CEs
   MPI_Irecv(&nums[0], 1, MPI_CHAR, recv_min_rank, MPI_ANY_TAG, MPI_COMM_WORLD, &req1);
   MPI_Irecv(&nums[1], 1, MPI_CHAR, recv_max_rank, MPI_ANY_TAG, MPI_COMM_WORLD, &req2);
   MPI_Wait(&req1, &stat1);
   MPI_Wait(&req2, &stat2);
   // sort two elements
   if (nums[0] > nums[1]) swap_nums(nums);
   // Send data to next CEs
   MPI_Isend(&nums[0], 1, MPI_CHAR, send_min_rank, MIN_TAG, MPI_COMM_WORLD, &req3);
   MPI_Isend(&nums[1], 1, MPI_CHAR, send_max_rank, MAX_TAG, MPI_COMM_WORLD, &req4);
   MPI_Wait(&req3, &stat3);
   MPI_Wait(&req4, &stat4);
}

/*
*  -------- MAIN ----------
*/
int main( int argc, char *argv[] ) {
   MPI_Init(&argc, &argv);

   MPI_Comm layer_comm;
   MPI_Status status;
   MPI_Request req1, req2, request;

   int layer = 1, world_rank, layer_rank, layer_size, world_size;
   unsigned char *buf, *sorted_buf, *nums;
   nums = (unsigned char *) malloc(2 *sizeof(unsigned char));

   MPI_Comm_rank( MPI_COMM_WORLD, &world_rank );
   MPI_Comm_size( MPI_COMM_WORLD, &world_size );
   
   // Tag processes with layer tag (will be used for splitting the communicator)
   if (world_rank < 4) {
      layer = 0;
   }

   if (world_rank > 9) {
      layer = 2;
   }

   // Split processes into layers (input (1x1) Block/ (2x2) Block / (4x4) Block)
   MPI_Comm_split(MPI_COMM_WORLD, layer, world_rank, &layer_comm);
   MPI_Comm_rank(layer_comm, &layer_rank);
   MPI_Comm_size(layer_comm, &layer_size);

   // Master process opens file and load its contents into buffer
   if (world_rank == MASTER) {
      FILE *fp = fopen("numbers", "rb");
      buf = (unsigned char *) malloc(BUF_SIZE * sizeof(unsigned char));
      fread(buf, sizeof(buf), 1, fp);
      fclose(fp);

      // Print values of unsorted buffer in prescribed format
      for (int i = 0; i < sizeof(buf); i++){
         printf("%hhu", buf[i]);
         if (i != 7) printf(" ");
      }
      printf("\n");
   }

   /* ---------------------------------------------------
   *     DISTRIBUTE INPUT VALUES INTO INPUT LAYER CEs
   * ---------------------------------------------------- */
   // Master process will distribute values into input layer CEs 
   MPI_Scatter(buf, 2, MPI_CHAR, nums, 2, MPI_CHAR, MASTER, layer_comm);

   // Clear memory of other CEs from random memory trash
   if (layer != 0) {
      nums[0] = 0;
      nums[1] = 0;
   }

   MPI_Barrier(MPI_COMM_WORLD);

   /* ---------------------------------------------------
   *                 1x1 BLOCK LOGIC
   * ---------------------------------------------------- */
   // Sort two input elements and send them to appropriate 2x2 Block CE
   if (layer == 0) {
      if (nums[0] > nums[1]) {
         swap_nums(nums);
      }
      int next_i = layer_rank < 2 ? 4 : 6;
      MPI_Isend(&nums[0], 1, MPI_CHAR, next_i, 1, MPI_COMM_WORLD, &req1);
      MPI_Isend(&nums[1], 1, MPI_CHAR, next_i+1, 1, MPI_COMM_WORLD, &req2);
      MPI_Wait(&req1, &status);
      MPI_Wait(&req2, &status);
   }

   /* ---------------------------------------------------
   *                 2x2 BLOCK LOGIC
   * ---------------------------------------------------- */
   if (layer == 1) {
      switch(layer_rank) {
         case 0:
            recv_process_send(0, 1, 10, 8, nums);
            break;
         case 1:
            recv_process_send(0, 1, 8, 13, nums);
            break;
         case 2:
            recv_process_send(2, 3, 10, 9, nums);
            break;
         case 3:
            recv_process_send(2, 3, 9, 13, nums);
            break;
         case 4:
            recv_process_send(4, 5, 12, 11, nums);
            break;
         case 5:
            recv_process_send(6, 7, 12, 11, nums);
            break;
         default:
            break;
      }
   }

   /* ---------------------------------------------------
   *                 4x4 BLOCK LOGIC
   * ---------------------------------------------------- */
   if (layer == 2) {
      switch(layer_rank) {
         case 0:
            recv_process_send(4, 6, MASTER, 14, nums);
            break;
         case 1:
            recv_process_send(8, 9, 14, 18, nums);
            break;
         case 2:
            recv_process_send(8, 9, 16, 15, nums);
            break;
         case 3:
            recv_process_send(5, 7, 15, MASTER, nums);
            break;
         case 4:
            recv_process_send(10, 11, 16, 17, nums);
            break;
         case 5:
            recv_process_send(12, 13, 17, 18, nums);
            break;
         case 6:
            recv_process_send(14, 12, MASTER, MASTER, nums);
            break;
         case 7:
            recv_process_send(14, 15, MASTER, MASTER, nums);
            break;
         case 8:
            recv_process_send(11, 15, MASTER, MASTER, nums);
            break;
         default:
            break;
      }
   }

   // Now master process should receive messages from CEs of the last instances
   if (world_rank == MASTER) {
      MPI_Request req1, req2, req3, req4, req5, req6, req7, req8;
      MPI_Status stat1, stat2, stat3, stat4, stat5, stat6, stat7, stat8;
      sorted_buf = (unsigned char *) malloc(BUF_SIZE * sizeof(unsigned char));

      // Receive data from last instance CEs
      MPI_Irecv(&sorted_buf[0], 1, MPI_CHAR, 10, MIN_TAG, MPI_COMM_WORLD, &req1);
      MPI_Irecv(&sorted_buf[1], 1, MPI_CHAR, 16, MIN_TAG, MPI_COMM_WORLD, &req2);
      MPI_Irecv(&sorted_buf[2], 1, MPI_CHAR, 16, MAX_TAG, MPI_COMM_WORLD, &req3);
      MPI_Irecv(&sorted_buf[3], 1, MPI_CHAR, 17, MIN_TAG, MPI_COMM_WORLD, &req4);
      MPI_Irecv(&sorted_buf[4], 1, MPI_CHAR, 17, MAX_TAG, MPI_COMM_WORLD, &req5);
      MPI_Irecv(&sorted_buf[5], 1, MPI_CHAR, 18, MIN_TAG, MPI_COMM_WORLD, &req6);
      MPI_Irecv(&sorted_buf[6], 1, MPI_CHAR, 18, MAX_TAG, MPI_COMM_WORLD, &req7);
      MPI_Irecv(&sorted_buf[7], 1, MPI_CHAR, 13, MAX_TAG, MPI_COMM_WORLD, &req8);

      MPI_Wait(&req1, &stat1);
      MPI_Wait(&req2, &stat2);
      MPI_Wait(&req3, &stat3);
      MPI_Wait(&req4, &stat4);
      MPI_Wait(&req5, &stat5);
      MPI_Wait(&req6, &stat6);
      MPI_Wait(&req7, &stat7);
      MPI_Wait(&req8, &stat8);
   }

   // Print contents of sorted buffer
   if (world_rank == MASTER) {
      for (int i = 0; i < sizeof(sorted_buf); i++) printf("%hhu\n", sorted_buf[i]);
   }

   // Free allocated memory of all CEs and master process
   free(nums);
   if (world_rank == MASTER) {
      free(buf);
      free(sorted_buf);
   }

   MPI_Finalize();
   return 0;
}
