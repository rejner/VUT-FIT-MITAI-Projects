/**
 * @file BatchMandelCalculator.h
 * @author Michal Rein <xreinm00@stud.fit.vutbr.cz>
 * @brief Implementation of Mandelbrot calculator that uses SIMD paralelization over small batches
 * @date 09.11.2021
 */
#ifndef BATCHMANDELCALCULATOR_H
#define BATCHMANDELCALCULATOR_H

#include <BaseMandelCalculator.h>

class BatchMandelCalculator : public BaseMandelCalculator
{
public:
    BatchMandelCalculator(unsigned matrixBaseSize, unsigned limit);
    ~BatchMandelCalculator();
    int * calculateMandelbrot();

private:
    int *data;
    float *xdata, *ydata, *rdata, *idata;
};

#endif