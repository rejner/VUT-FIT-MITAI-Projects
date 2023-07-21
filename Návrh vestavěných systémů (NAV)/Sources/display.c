/* NAV Project - Distance measurement with ultrasound sensor
 * Author:		Michal Rein (xreinm00)
 * Date:		13.03.2022
 * File:		display.c
 * Description: Method implementation for display manipulation.
 */

#include "MK60D10.h"
#include "display.h"


/* Reset display */
void reset_display() {
	PTA->PDOR &= ~PTA_SEGMENTS_MASK;
	PTD->PDOR &= ~PTD_SEGMENTS_MASK;
}

/* Show number
 * @param num Number to be displayed.
 */
void show_number(int num) {

	reset_display();
	switch(num) {
		case 0:
			PTA->PDOR |= PTA_SEGMENTS_MASK & ZERO;
			PTD->PDOR |= PTD_SEGMENTS_MASK & ZERO;
			break;
		case 1:
			PTA->PDOR |= PTA_SEGMENTS_MASK & ONE;
			PTD->PDOR |= PTD_SEGMENTS_MASK & ONE;
			break;
		case 2:
			PTA->PDOR |= PTA_SEGMENTS_MASK & TWO;
			PTD->PDOR |= PTD_SEGMENTS_MASK & TWO;
			break;
		case 3:
			PTA->PDOR |= PTA_SEGMENTS_MASK & THREE;
			PTD->PDOR |= PTD_SEGMENTS_MASK & THREE;
			break;
		case 4:
			PTA->PDOR |= PTA_SEGMENTS_MASK & FOUR;
			PTD->PDOR |= PTD_SEGMENTS_MASK & FOUR;
			break;
		case 5:
			PTA->PDOR |= PTA_SEGMENTS_MASK & FIVE;
			PTD->PDOR |= PTD_SEGMENTS_MASK & FIVE;
			break;
		case 6:
			PTA->PDOR |= PTA_SEGMENTS_MASK & SIX;
			PTD->PDOR |= PTD_SEGMENTS_MASK & SIX;
			break;
		case 7:
			PTA->PDOR |= PTA_SEGMENTS_MASK & SEVEN;
			PTD->PDOR |= PTD_SEGMENTS_MASK & SEVEN;
			break;
		case 8:
			PTA->PDOR |= PTA_SEGMENTS_MASK & EIGHT;
			PTD->PDOR |= PTD_SEGMENTS_MASK & EIGHT;
			break;
		case 9:
			PTA->PDOR |= PTA_SEGMENTS_MASK & NINE;
			PTD->PDOR |= PTD_SEGMENTS_MASK & NINE;
			break;
		default:
			break;
	}

}

/* Show dot */
void show_dot() {
	PTA->PDOR |= DOT;
}

/* Perform display column selection.
 * @param index 0-3 index of column to be selected.
 */
void select_display_column(int index) {
	PTD->PDOR |= DISPLAY_COL_MASK;
	switch(index) {
		case 0:
			PTD->PDOR &= ~FIRST_COL;
			break;
		case 1:
			PTD->PDOR &= ~SECOND_COL;
			break;
		case 2:
			PTD->PDOR &= ~THIRD_COL;
			break;
		case 3:
			PTD->PDOR &= ~FOURTH_COL;
			break;
		default:
			break;
	}
}
