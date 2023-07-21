/**
 * @file LineMandelCalculator.h
 * @author Michal Rein <xreinm00@stud.fit.vutbr.cz>
 * @brief Implementation of Mandelbrot calculator that uses SIMD paralelization over lines
 * @date 09.11.2021
 */

#include <BaseMandelCalculator.h>

class LineMandelCalculator : public BaseMandelCalculator
{
public:
    LineMandelCalculator(unsigned matrixBaseSize, unsigned limit);
    ~LineMandelCalculator();
    int *calculateMandelbrot();

private:
    int *data;
    float *xdata, *ydata, *idata, *rdata;
};