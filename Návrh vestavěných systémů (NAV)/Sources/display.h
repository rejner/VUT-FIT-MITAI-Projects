/* NAV Project - Distance measurement with ultrasound sensor
 * Author:		Michal Rein (xreinm00)
 * Date:		13.03.2022
 * File:		display.h
 * Description: Contains mapping of LED display segments and numbers
 */

#ifndef SOURCES_DISPLAY_H_
#define SOURCES_DISPLAY_H_

// LED Display column mapping
#define DISPLAY_COL_MASK 		0x3300		// xx11 xx11 0000 0000
#define FIRST_COL  				0x100		// PTD 8
#define SECOND_COL				0x2000		// PTD 13
#define THIRD_COL  				0x1000		// PTD 12
#define FOURTH_COL 				0x200		// PTD 9

#define BUFFER_SIZE				5			// 4 numbers + '.' symbol

// Segments mapping
#define PTA_SEGMENTS_MASK		0xFC0		// PTA 6-11 	(1111_1100_0000)
#define PTD_SEGMENTS_MASK		0xC000		// PTD 14-15    (1100_0000_0000_0000)
#define UPPER_LEFT    			0x00080
#define BOTTOM_LEFT  			0x00040
#define UPPER_RIGHT   			0x00200
#define BOTTOM_RIGHT 			0x04000
#define UP         				0x00800
#define BOTTOM     				0x00400
#define CENTER     				0x08000
#define DOT        				0x00100


// Numbers mapping on segments
#define ZERO	(BOTTOM_LEFT	| UPPER_LEFT 	| UP            | BOTTOM       | BOTTOM_RIGHT | UPPER_RIGHT)
#define ONE		(UPPER_RIGHT	| BOTTOM_RIGHT)
#define TWO		(UP 			| UPPER_RIGHT 	| CENTER 		| BOTTOM_LEFT  | BOTTOM)
#define THREE	(UP 			| UPPER_RIGHT 	| BOTTOM_RIGHT  | BOTTOM       | CENTER)
#define FOUR	(UPPER_LEFT 	| CENTER 		| UPPER_RIGHT   | BOTTOM_RIGHT)
#define FIVE	(UPPER_LEFT 	| UP 			| CENTER        | BOTTOM_RIGHT | BOTTOM)
#define SIX		(UP 			| UPPER_LEFT 	| CENTER        | BOTTOM_RIGHT | BOTTOM       | BOTTOM_LEFT)
#define SEVEN	(UP 			| UPPER_RIGHT 	| BOTTOM_RIGHT)
#define EIGHT	(BOTTOM_LEFT 	| UPPER_LEFT 	| UP            | BOTTOM       | BOTTOM_RIGHT | UPPER_RIGHT | CENTER)
#define NINE	(UPPER_LEFT 	| UP 			| BOTTOM        | BOTTOM_RIGHT | UPPER_RIGHT  | CENTER)

void reset_display();

void show_number(int num);

void show_dot();

void select_display_column(int index);


#endif /* SOURCES_DISPLAY_H_ */
