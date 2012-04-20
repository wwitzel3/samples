/*
 *  SimpleClass.cpp
 *  pcdr-test
 *
 *  Created by Wayne Witzel III on 8/3/10.
 *  Copyright 2010 __MyCompanyName__. All rights reserved.
 *
 */

#include <iostream>

int x = 3;
int y = 4;



class SimpleClass {
	
public:
	static int x;
	int y;
	
	SimpleClass() : y(2) {}
	
	static void run() {
		int x = 10;
		
		// Part a
		std::cout << x << std::endl;
		
		// Part b
		std::cout << SimpleClass::x << std::endl;
		
		// Part c
		std::cout << ::x << std::endl;
		
		SimpleClass simpleClass;
		simpleClass.printY(20);
		
	}
	
	
	
	void printY(int y) {
		
		// Part d
		std::cout << y << std::endl;
		
		// Part e
		std::cout << this->y << std::endl;
		
		// Part f
		std::cout << ::y << std::endl;
		
	}
	
};



int SimpleClass::x = 1;

/*
int main(int argc, char** argv) {
	SimpleClass::run();
	
}
*/
