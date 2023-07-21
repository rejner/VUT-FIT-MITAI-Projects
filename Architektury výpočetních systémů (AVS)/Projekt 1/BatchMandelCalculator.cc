/**
 * @file BatchMandelCalculator.cc
 * @author Michal Rein <xreinm00@stud.fit.vutbr.cz>
 * @brief Implementation of Mandelbrot calculator that uses SIMD paralelization over small batches
 * @date 09.11.2021
 */

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

#include <stdlib.h>
#include <stdexcept>

#include "BatchMandelCalculator.h"

#define BATCH_SIZE 16

BatchMandelCalculator::BatchMandelCalculator (unsigned matrixBaseSize, unsigned limit) :
	BaseMandelCalculator(matrixBaseSize, limit, "BatchMandelCalculator")
{
	// allocate & prefill memory
	data = (int *)(aligned_alloc(64, height * width * sizeof(int)));
	xdata = (float *)(aligned_alloc(64, height * width * sizeof(float)));
	ydata = (float *)(aligned_alloc(64, height * width * sizeof(float)));
	rdata = (float *)(aligned_alloc(64, height * width * sizeof(float)));
	idata = (float *)(aligned_alloc(64, height * width * sizeof(float)));
}

BatchMandelCalculator::~BatchMandelCalculator() {
	// cleanup the memory
	free(data);
	free(xdata);
	free(ydata);
	free(rdata);
	free(idata);
	data, xdata, ydata = NULL;
}

int * BatchMandelCalculator::calculateMandelbrot () {

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

	const int batch_size = BATCH_SIZE;
	const int N = aux_width / batch_size;

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


	// iterate through entire height
	for (int i = 0; i < aux_height; i++){
		
		for (int l = 0; l < limit; l++) {
			int num_of_finished = aux_width;
			// TILE index
			for (int ti = 0; ti < N; ti++) {
				// Local index
				const int step = (i * aux_width) + (ti * batch_size);
				#pragma omp simd reduction(-:num_of_finished) simdlen(512)
				for (int li = 0; li < batch_size; li++) {
					
					// calculate values of each element for given depth level  
					float r2 = prdata[step + li] * prdata[step + li];
					float i2 = pidata[step + li] * pidata[step + li];
					
					// when end condition isn't satisfied, increment element's final value,
					// else modify variable for breaking out of row processing
					if (r2 + i2 > 4.0f) {
						num_of_finished -= 1;
					} else {
						pidata[step + li] = 2.0f * prdata[step + li] * pidata[step + li] + pydata[step + li];
						prdata[step + li] = r2 - i2 + pxdata[step + li];
						pdata[step + li]++;
					}
				}
			}
			if (num_of_finished <= 0) break;
		}	
	}

	return data;
}