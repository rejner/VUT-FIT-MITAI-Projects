
/* NAV Project - Distance measurement with ultrasound sensor
 * Author:		Michal Rein (xreinm00)
 * Date:		09.04.2022
 * File:		main.c
 */

#include "MK60D10.h"
#include "display.h"
#include <stdio.h>
#include <stdlib.h>

float distance = 0.0;				// calculated distance
static int receiving_signal = 0;	// FLAG indicating sensor transmission
static unsigned int end = 0;		// time measurement of ECHO pulse length

// Display mode (measurement can be shown in different metrics)
#define SW6 0x800		// PTE 11 (mode change button)
int display_mode = 0;
enum {
	DISPLAY_MODE_CENTIMETERS,
	DISPLAY_MODE_METERS,
	DISPLAY_MODE_MILLIMETERS
};

/* Sensor PINs mapping */
#define TRIGGER  	    0x08000000	// PTA 27
#define ECHO   			0x20000000	// PTA 29

/* Delay method */
void delay(long delay) {
	for(long i = 0; i < delay; i++){}
}

/* Initialize the MCU */
void mcu_init(void) {
    MCG_C4       |= ( MCG_C4_DMX32_MASK | MCG_C4_DRST_DRS(0x01) );
    WDOG_STCTRLH &= ~WDOG_STCTRLH_WDOGEN_MASK;
}

/* Flex timer init */
void FTM1_TIMER_Init() {
	// System Clock Gating Control Register 6
	SIM_SCGC6 |= SIM_SCGC6_FTM1_MASK;	// FTM Clock Gate Control - clock enable
	FTM1_SC |= 0xD; 					// Enable FTM with system clock with 32 prescale (1101)
	FTM1_CNTIN |= 0x0; 					// FTM1_CNT -> current val
}

/* PORTA interrupt request handler (from sensor)
 * Requests are handled for ECHO PIN which will stop current measurement sequence */
void PORTA_IRQHandler(void) {

	if ((PORTA->ISFR & ECHO) && !(GPIOA_PDIR & ECHO))
	{
		receiving_signal = 0; // stop measurement
		PORTA->ISFR = ~0;     // reset interrupt flag
	}
}

/* PORTE interrupt request handler
 * Requests are handled for button SW6 which change modes */
void PORTE_IRQHandler(void) {

	// Metrics mode button
	if (PORTE->ISFR & SW6) {
		display_mode = display_mode == 2 ? 0 : ++display_mode;
		PTB->PDOR     = GPIO_PDOR_PDO(0x3C); // turn all LEDs OFF
		// light indicator LED
		switch(display_mode) {
		case DISPLAY_MODE_METERS:
			PTB->PDOR = GPIO_PDOR_PDO(0x34);
			break;
		case DISPLAY_MODE_MILLIMETERS:
			PTB->PDOR = GPIO_PDOR_PDO(0x2C);
			break;
		case DISPLAY_MODE_CENTIMETERS:
			PTB->PDOR = GPIO_PDOR_PDO(0x38); // 00x- --00
			break;
		default:
			break;
		}
	}

	PORTE->ISFR = ~0;     // reset interrupt flag

}



/* Initialize required ports */
void init_ports() {
	// Enable clocks
	SIM->SCGC5 = SIM_SCGC5_PORTA_MASK | SIM_SCGC5_PORTB_MASK | SIM_SCGC5_PORTE_MASK | SIM_SCGC5_PORTD_MASK;
	NVIC_ClearPendingIRQ(PORTA_IRQn);      // Clear PORTA pending interrupt requests
	NVIC_EnableIRQ(PORTA_IRQn);            // Enable PORTA interrupts

	/****************************
	 * Sensor PINs settings
	 ****************************/
	// PTA_29 = Sensor Echo PIN
	PORTA_PCR(29) = ( PORT_PCR_ISF(0x01)   // Interrupt status flag
					 | PORT_PCR_IRQC(0x0A) // Interrupt on falling edge
					 | PORT_PCR_MUX(0x01)  // Pin Mux Control set to GPIO
					 | PORT_PCR_PE(0x01)   // Enable pull resistor
					 | PORT_PCR_PS(0x01)); // Choose Pull-Up

	// PTA 27 = Sensor Trigger PIN
	PORTA_PCR(27) = PORT_PCR_MUX(0x01);	   // Pin Mux Control set to GPIO
	PTA->PDOR &= ~TRIGGER;				   // Reset output register


	/****************************
	 * PORT settings for display
	 ****************************/
	// Set all required PORTA pins to GPIO (6-11)
	for (int i = 6; i <= 11; i++) {
		PORTA_PCR(i) = PORT_PCR_MUX(0x01);
	}

	// Same for PORTD (8-9, 12-15)
	PORTD_PCR(8) = PORT_PCR_MUX(0x01);
	PORTD_PCR(9) = PORT_PCR_MUX(0x01);
	for (int i = 12; i <= 15; i++) {
		PORTD_PCR(i) = PORT_PCR_MUX(0x01);
	}

    // PORT B
	PORTB->PCR[2] = PORT_PCR_MUX(0x01); // D12 LED
	PORTB->PCR[3] = PORT_PCR_MUX(0x01); // D11 LED
	PORTB->PCR[4] = PORT_PCR_MUX(0x01); // D10 LED
    PORTB->PCR[5] = PORT_PCR_MUX(0x01); // D9  LED
    PTB->PDDR 	  = GPIO_PDDR_PDD(0x3C);
    PTB->PDOR     = GPIO_PDOR_PDO(0x38); // turn all LEDs OFF except D12 (default mode)| 0011 1100

    // PORT E
	NVIC_ClearPendingIRQ(PORTE_IRQn);      // Clear PORTE pending interrupt requests
	NVIC_EnableIRQ(PORTE_IRQn);            // Enable PORTE interrupts
	// PTE_11 = SW6 button (button for chaning display modes)
	PORTE_PCR(11) = ( PORT_PCR_ISF(0x01)   // Interrupt status flag
					 | PORT_PCR_IRQC(0x09) // Interrupt when logic 0
					 | PORT_PCR_MUX(0x01)  // Pin Mux Control set to GPIO
					 | PORT_PCR_PE(0x01)   // Enable pull resistor
					 | PORT_PCR_PS(0x01)); // Choose Pull-Up

	// set all display PINs + TRIGGER as output
	PTA->PDDR = GPIO_PDDR_PDD(0x8001FC0);
	PTD->PDDR = GPIO_PDDR_PDD(0xF300);


}

/* Display measured distance on display
 * @param distance Value to be displayed.
 */
void display_measurement(float distance) {

	// Change metrics based on currently active mode
	switch(display_mode) {
	case DISPLAY_MODE_METERS:
		distance /= 100;
		break;
	case DISPLAY_MODE_MILLIMETERS:
		distance *= 10;
		break;
	default:
		break;
	}

	int column = 0; 							// column index
	char buffer[BUFFER_SIZE];
	gcvt(distance, BUFFER_SIZE, buffer);		// convert float to char* (from <stdlib.h>)
	for (int i = 0; i < BUFFER_SIZE; i++) {		// iterate over char* buffer
		if (buffer[i] == '.') continue;			// '.' char will be skipped (already displayed in previous column)
		select_display_column(column);			// select display segment
		show_number(buffer[i] - '0');			// subtracting number in char representation from '0' will result in integer value of given number
		if (i < 3 && buffer[i+1] == '.') {		// if next character is '.', display it with current number
			show_dot();
		}
		column++;
		delay(10000);
	}
}

/* Initialize and perform measurement sequence
 * @param storage 				Pointer for storing measurement result.
 * @param distance_per_usec		Distance in cm/us
 */
void start_measurement(float *storage, float distance_per_usec) {

	// Put trigger into stable 0
	PTA->PDOR &= ~TRIGGER;
	delay(100); // wait for around 100 ticks * 20ns =  +- 2us

	// Send TRIGGER pulse to sensor
	PTA->PDOR |= TRIGGER;
	delay(500); // wait for around 500 ticks * 20ns =  +- 10us
	PTA->PDOR &= ~TRIGGER;

	// Wait for ECHO PIN to be set by device to 1
	while (!(PTA->PDIR & ECHO)){}

	FTM1_CNT |= 0x00; 				// reset counter value
	receiving_signal = 1;			// set receiving echo FLAG
	while(receiving_signal) {		// wait for IQR from PORT A (will set receiving_signal to 0)
		end = FTM1_CNT;				// save current flex counter value
	}

	// Convert counter ticks (generated by flex timer) to microseconds
	// ticks_in_us = 1000 / (tick period in nanoseconds)
	// Example:
	// 50Mhz -> 20ns/tick, with prescale 32 -> 640ns/tick
	// Each tick = 640ns -> ticks_total * 0.64 = microseconds total
	float ticks_to_us = (float) (end * 0.64);
	*storage = (float) (ticks_to_us * distance_per_usec) / 2;
}

/* MAIN */
int main(void) {

	mcu_init();
	init_ports();
	FTM1_TIMER_Init();

	// Calculate distance per microsecond.
	// Providing temperature measurement can improve accuracy.
	float speed_of_sound = 331.1 + (0.606 * 24.0);
	float dist_per_usec = speed_of_sound / 10000.0; // 1m/s = 0.0001 cm/us

	display_mode = DISPLAY_MODE_CENTIMETERS;
	PTB->PDOR = GPIO_PDOR_PDO(0x38);			// Set correct LED config

	long counter = 0;
    for (;;) {
    	// periodically perform measurement
    	if (counter % 10 == 0) {
    		start_measurement(&distance, dist_per_usec);
    	}
    	if (distance < 200 && distance > 0) {
    		display_measurement(distance);
    	} else {
    		reset_display();
    	}

    	counter++;
    }
    /* Never leave main */
    return 0;
}
////////////////////////////////////////////////////////////////////////////////
// EOF
////////////////////////////////////////////////////////////////////////////////
