/**
 * @file    tree_mesh_builder.h
 *
 * @author  Michal Rein <xreinm00@stud.fit.vutbr.cz>
 *
 * @brief   Parallel Marching Cubes implementation using OpenMP tasks + octree early elimination
 *
 * @date    17.12.2021
 **/

#ifndef TREE_MESH_BUILDER_H
#define TREE_MESH_BUILDER_H

#include "base_mesh_builder.h"

class TreeMeshBuilder : public BaseMeshBuilder
{
public:
    TreeMeshBuilder(unsigned gridEdgeSize);
    ~TreeMeshBuilder();

protected:
    unsigned marchCubes(const ParametricScalarField &field);
    float evaluateFieldAt(const Vec3_t<float> &pos, const ParametricScalarField &field);
    void emitTriangle(const Triangle_t &triangle);
    unsigned parseTree(unsigned int gridSize, const Vec3_t<float> &pos, const ParametricScalarField &field);

    // For debugging purposes
    unsigned parseTreeLast(float cubeEdgeSize, const Vec3_t<float> &pos, const ParametricScalarField &field);
    const Triangle_t *getTrianglesArray() const { return mTriangles.data(); }
    std::vector<Triangle_t> mTriangles;
    std::vector<Triangle_t> *mTrianglesArray;
};

#endif // TREE_MESH_BUILDER_H
