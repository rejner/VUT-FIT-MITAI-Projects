/**
 * @file    tree_mesh_builder.cpp
 *
 * @author  Michal Rein <xreinm00@stud.fit.vutbr.cz>
 *
 * @brief   Parallel Marching Cubes implementation using OpenMP tasks + octree early elimination
 *
 * @date    17.12.2021
 **/

#include <iostream>
#include <math.h>
#include <limits>
#include <omp.h>

#include "tree_mesh_builder.h"

TreeMeshBuilder::TreeMeshBuilder(unsigned gridEdgeSize)
    : BaseMeshBuilder(gridEdgeSize, "Octree")
{
    // declare array of vectors, each thread will store triangles into its separate vector
    mTrianglesArray = new std::vector<Triangle_t>[omp_get_max_threads()];
}

TreeMeshBuilder::~TreeMeshBuilder()
{
}

// prepsat float na int
unsigned TreeMeshBuilder::parseTreeLast(float gridSize, const Vec3_t<float> &pos, const ParametricScalarField &field) {
    unsigned totalTriangles = 0;
    int halfGridSize = gridSize / 2;
    float cubeEdgeSize = (float) halfGridSize;

    // Test if there is possibly any triangle to render
    Vec3_t<float> midPoint((pos.x + cubeEdgeSize)*mGridResolution,
                            (pos.y + cubeEdgeSize)*mGridResolution,
                            (pos.z + cubeEdgeSize)*mGridResolution);

    // Calculate condition whether there is a surface withing cube or not.
    // If surface isn't present within the cube, it's useless to parse the tree any further
    if (evaluateFieldAt(midPoint, field) > (field.getIsoLevel() + (sqrtf(3.0f)/2.0f)*cubeEdgeSize*mGridResolution)){
        return 0; // Note: expression ...)cubeEdgeSize*mGridResolution causes holes in the model
    }

    // Consider smallest possible cube to be 1 unit long
    // If condition is satisfied, build final cube from it.
    if (cubeEdgeSize <= 1) {
        //#pragma omp critical
        totalTriangles = buildCube(pos, field);
        return totalTriangles;
    }

    // Now, lets split current cube into 8 sub-cubes
    /*  x, y, z
        0, 0, 1,
        1, 1, 0,
        0, 1, 1,
        1, 0, 0,
        0, 1, 0,
        1, 0, 1,
        0, 0, 0,
        1, 1, 1,
    */
    for (int i = 0; i < 8; i++) {
        //printf("Thread rank: %d, creating task with i=%d\n", omp_get_thread_num(), i);
        // #pragma omp task shared(totalTriangles, cubeEdgeSize) firstprivate(i)
        #pragma omp task default(none) firstprivate(i) \
        shared(pos, cubeEdgeSize, halfGridSize, field, totalTriangles)
        {
            //printf("Thread rank: %d\n", omp_get_thread_num());
            Vec3_t<float> subCubePos(pos.x + (i%2)*cubeEdgeSize,
                        pos.y + (i < 2 ? (i%2)*cubeEdgeSize : i < 6 ? ((i+1)%2)*cubeEdgeSize : (i%2)*cubeEdgeSize),
                        pos.z + (i < 4 ? ((i+1)%2)*cubeEdgeSize : (i%2)*cubeEdgeSize));
            
            unsigned totalSubTriangles = parseTree(halfGridSize, subCubePos, field);
            #pragma omp atomic
            totalTriangles += totalSubTriangles;
        }
    }
    #pragma omp taskwait
    
    return totalTriangles;
}

unsigned TreeMeshBuilder::parseTree(unsigned int gridSize, const Vec3_t<float> &pos, const ParametricScalarField &field) {    
    unsigned totalTriangles = 0;
    int halfGridSize = gridSize / 2;
    float cubeEdgeSize = (float) halfGridSize;

    // Consider smallest possible cube to be 1 unit long
    // If condition is satisfied, build final cube from it.
    if (gridSize > 1) {
        // Calculate middle point of current cube
        Vec3_t<float> midPoint((pos.x + cubeEdgeSize)*mGridResolution,
                               (pos.y + cubeEdgeSize)*mGridResolution,
                               (pos.z + cubeEdgeSize)*mGridResolution);

        // Calculate condition whether there is a surface withing cube or not.
        // If surface isn't present within the cube, it's useless to parse the tree any further
        if (evaluateFieldAt(midPoint, field) > mIsoLevel + (sqrtf(3.0f)/2.0f)*gridSize*mGridResolution){
            return 0; // Note: expression ...)cubeEdgeSize*mGridResolution causes holes in the model
        }
        

        // Now, lets split current cube into 8 sub-cubes
        /*  x, y, z
            0, 0, 1,
            1, 1, 0,
            0, 1, 1,
            1, 0, 0,
            0, 1, 0,
            1, 0, 1,
            0, 0, 0,
            1, 1, 1,
        */
        
        for (int i = 0; i < 8; i++) {
            //printf("Thread rank: %d, creating task with i=%d\n", omp_get_thread_num(), i);
            
            #pragma omp task shared(totalTriangles, field) firstprivate(i, cubeEdgeSize, halfGridSize)
            {   
                Vec3_t<float> subCubePos(pos.x + (i%2)*cubeEdgeSize,
                            pos.y + (i < 2 ? (i%2)*cubeEdgeSize : i < 6 ? ((i+1)%2)*cubeEdgeSize : (i%2)*cubeEdgeSize),
                            pos.z + (i < 4 ? ((i+1)%2)*cubeEdgeSize : (i%2)*cubeEdgeSize));
                
                unsigned subCubeTriangles = parseTree(halfGridSize, subCubePos, field);

                #pragma omp atomic
                totalTriangles += subCubeTriangles;
            }
            
        }
        
        
    } else {
        unsigned triangles = buildCube(pos, field); 
        
        #pragma omp critical
        totalTriangles += triangles; 
    }

    #pragma omp taskwait
    return totalTriangles;
}



unsigned TreeMeshBuilder::marchCubes(const ParametricScalarField &field)
{
    // Suggested approach to tackle this problem is to add new method to
    // this class. This method will call itself to process the children.
    // It is also strongly suggested to first implement Octree as sequential
    // code and only when that works add OpenMP tasks to achieve parallelism.
    
    unsigned totalTriangles = 0;

    // Start recursive process of parsing tree, cubeEdgeSize will be equal to size of entire grid because
    // we start from 1 huge cube which is represented by entire grid space.
    #pragma omp parallel
    {
        #pragma omp single
        {
            totalTriangles = parseTree(mGridSize, Vec3_t<float>(0, 0, 0), field);
        }
    }

    // Merge all partial vector fields into one which is then stored into output file
    for (int i = 0; i < omp_get_max_threads(); i++) {
        mTriangles.insert(mTriangles.end(), mTrianglesArray[i].begin(), mTrianglesArray[i].end());
    }
    

    // Return total number of triangles generated.
    return totalTriangles;
}

float TreeMeshBuilder::evaluateFieldAt(const Vec3_t<float> &pos, const ParametricScalarField &field)
{
    // 1. Store pointer to and number of 3D points in the field
    //    (to avoid "data()" and "size()" call in the loop).
    const Vec3_t<float> *pPoints = field.getPoints().data();
    const unsigned count = unsigned(field.getPoints().size());

    float value = std::numeric_limits<float>::max();

    // 2. Find minimum square distance from points "pos" to any point in the
    //    field.
    for(unsigned i = 0; i < count; ++i)
    {
        float distanceSquared  = (pos.x - pPoints[i].x) * (pos.x - pPoints[i].x);
        distanceSquared       += (pos.y - pPoints[i].y) * (pos.y - pPoints[i].y);
        distanceSquared       += (pos.z - pPoints[i].z) * (pos.z - pPoints[i].z);

        // Comparing squares instead of real distance to avoid unnecessary
        // "sqrt"s in the loop.
        value = std::min(value, distanceSquared);
    }

    // 3. Finally take square root of the minimal square distance to get the real distance
    return sqrt(value);
}

void TreeMeshBuilder::emitTriangle(const BaseMeshBuilder::Triangle_t &triangle)
{
    mTrianglesArray[omp_get_thread_num()].push_back(triangle);
}
