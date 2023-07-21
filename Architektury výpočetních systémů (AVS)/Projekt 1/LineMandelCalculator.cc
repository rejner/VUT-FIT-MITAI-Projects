/**
 * @file LineMandelCalculator.cc
 * @author Michal Rein <xreinm00@stud.fit.vutbr.cz>
 * @brief Implementation of Mandelbrot calculator that uses SIMD paralelization over lines
 * @date 09.11.2021
 */
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

#include <stdlib.h>


#include "LineMandelCalculator.h"

LineMandelCalculator::LineMandelCalculator (unsigned matrixBaseSize, unsigned limit) :
	BaseMandelCalculator(matrixBaseSize, limit, "LineMandelCalculator")
{
	// allocate & prefill memory
	
	data = (int *)(aligned_alloc(64, height * width * sizeof(int)));
	xdata = (float *)(aligned_alloc(64, height * width * sizeof(float)));
	ydata = (float *)(aligned_alloc(64, height * width * sizeof(float)));
	rdata = (float *)(aligned_alloc(64, height * width * sizeof(float)));
	idata = (float *)(aligned_alloc(64, height * width * sizeof(float)));
}

LineMandelCalculator::~LineMandelCalculator() {
	// cleanup the memory
	free(data);
	free(xdata);
	free(ydata);
	free(rdata);
	free(idata);
	data, xdata, ydata = NULL;
}


int * LineMandelCalculator::calculateMandelbrot () {
	
	int *pdata = data;
	float *prdata = rdata;
	float *pidata = idata;
	float *pxdata = xdata;
	float *pydata = ydata;

	// define constants to make Intel Advisor happy
	const int total_size = height * width;
	const int aux_width = width;
	const int aux_height = height;
	const double aux_dx = dx;
	const double aux_dy = dy;

	// fill data with default values
	#pragma omp simd
	for (int dl = 0; dl < total_size; dl++){
		data[dl] = 0;
	}

	for (int i = 0; i < aux_height; i++) {
		// pre-calculate real and imag values
		#pragma omp simd
		for (int j = 0; j < aux_width; j++) {
			xdata[(i * aux_width) + j] = x_start + j * aux_dx; // store real value
			ydata[(i * aux_width) + j] = y_start + i * aux_dy; // store imaginary value
			rdata[(i * aux_width) + j] = x_start + j * aux_dx;
			idata[(i * aux_width) + j] = y_start + i * aux_dy;
		}
	}
	
	// iterate through all rows
	for (int i = 0; i < aux_height; i++)
	{

		for (int l = 0; l < limit; l++) {
			int num_of_finished = aux_width;
			const int step = i * aux_width;
			// calculate values of each element for given depth level  
			#pragma omp simd reduction(-:num_of_finished)
			for (int k = 0; k < aux_width; k++)
			{	
				float r2 = prdata[step + k] * prdata[step + k];
				float i2 = pidata[step + k] * pidata[step + k];

				// when end condition isn't satisfied, increment element's final value,
				// else modify variable for breaking out of row processing
				if (r2 + i2 > 4.0f) {
					num_of_finished -= 1;
				} else {
					pidata[step + k] = 2.0f * prdata[step + k] * pidata[step + k] + pydata[step + k];
					prdata[step + k] = r2 - i2 + pxdata[step + k];
					pdata[step + k]++;
				}
			}

			if (num_of_finished <= 0) break;
		}
	}

	return data;

	// Výpis dat
	/*
	std::cout << "Printing data: \n";
	for (int i = 0; i < height; i++) {
		for (int j = 0; j < width; j++) {
			std::cout << data[i*width + j] << " ";
		}
		std::cout << "\n";
	}
	*/
	
}


/*
// So far the fastest implementation, but without loop swapping (black magic included)
template <typename T>
static inline int mandelbrot(T real, T imag, int limit)
{
	T zReal = real;
	T zImag = imag;
	int i = 0;
	
	for (; i < limit; ++i)
	{
		T r2 = zReal * zReal;
		T i2 = zImag * zImag;

		zImag = 2.0f * zReal * zImag + imag;
		zReal = r2 - i2 + real;

		if (r2 + i2 > 4.0f) break;
			//break; // break: -90 ms, last line: -110 ms 
	}

	return i;
}


int * LineMandelCalculator::calculateMandelbrot () {
	int *pdata = data;
	
	// define constants to make Intel Advisor happy
	const int total_size = height * width;
	const int aux_width = width;
	const int aux_height = height;
	const double aux_dx = dx;
	const double aux_dy = dy;

	for (int i = 0; i < height; i++)
	{
		// pre-calculate real and imag values
		for (int j = 0; j < width; j++) // -20 ms
		{
			xdata[j] = x_start + j * dx; // store real value
			ydata[j] = y_start + i * dy; // store imaginary value
		}

		#pragma omp simd // -1400 ms
		for (int k = 0; k < width; k++)
		{			
			int value = mandelbrot(xdata[k], ydata[k], limit);
			*(pdata++) = value;
		}
	}

	return data;
}
*/
