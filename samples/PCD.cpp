/*
 *  PCD.cpp
 *  pcdr-test
 *
 *  Created by Wayne Witzel III on 8/3/10.
 *  Copyright 2010 __MyCompanyName__. All rights reserved.
 *
 */

/*
 a) Implement a copy constructor.
 
 b) Implement an assignment operator.
 
 c) Implement a destructor.
 
 d) In main, which method in DataStructure is implicitly called for the following line? firstDataSet = secondDataSet;
 Assignment operator
 
 e) In main, which method in DataStructure is implicitly called for the following line? DataStructure thirdDataSet(secondDataSet);
 Copy constructor
 
 f) In main, which method in DataStructure is implicitly called for the following line? DataStructure fourthDataSet = secondDataSet;
 Copy constructor
 
 g) What type of data structure is this?
 Linked list
 
*/

#include <cstdlib>

namespace PCD {
	
	struct Node {
		Node(int value): _nextNode(NULL), _data(value) {}
		Node* _nextNode;
		int _data;
	};             
	
	
	
	class DataStructure {
		
	public:
		DataStructure();
		~DataStructure();
		
		DataStructure(const DataStructure&);
		
		// ***** TODO: write the assignment operator (part b) ***** //
		DataStructure& operator=(const DataStructure& ds) {
			if (this != &ds) {
				Node* _current = ds._root;
				while (_current->_nextNode != NULL) {
					append(_current->_data);
					_current = _current->_nextNode;
				}
			}
			return *this;
		}
		
		// appends a value to the end of the data structure
		void append(int value);
		
	private:
		Node* _root;
	};
	
	
	
	DataStructure::DataStructure(): _root(NULL) { }
	
	
	
	void DataStructure::append(int value) {
		
		if (_root == NULL) {
			_root = new Node(value);
			return;
			
		}
		
		Node* currentNode = _root;
		while (currentNode->_nextNode != NULL) {
			currentNode = currentNode->_nextNode;
			
		}
		currentNode->_nextNode = new Node(value);
		
	}
	
	
	
	// ***** TODO: write the copy constructor (part a) ***** //
	DataStructure::DataStructure(const DataStructure& ds) {
		Node* _current = ds._root;
		Node* _new = NULL;
		if (_current != NULL) _new = new Node(_current->_data);
		
		while (_current->_nextNode != NULL) {
			_current = _current->_nextNode;
			_new->_nextNode = new Node(_current->_data);
		}
		_root = _new;
	}
	
	// ***** TODO: write the destructor (part c) ***** //
	DataStructure::~DataStructure(void) {
		Node* _current = _root;
		Node* _last = NULL;
		
		while (_current->_nextNode != NULL) {
			_last = _current;
			_current = _current->_nextNode;
			
			if (_last) delete _last;
		}
		_current = NULL;
		_last = NULL;
	}
	
	
	
	
} // namespace PCD



using namespace PCD;


/*
int main ( int argc, char * argv[]) {
	
	
	
	DataStructure firstDataSet;
	firstDataSet.append(3);
	firstDataSet.append(0);
	firstDataSet.append(22);
	
	DataStructure secondDataSet;
	secondDataSet.append(5);
	secondDataSet.append(87);
	secondDataSet.append(9);
	
	
	// Part d refers to this line
	firstDataSet = secondDataSet;
	
	// Part e refers to this line
	DataStructure thirdDataSet(secondDataSet);
	
	
	// Part 6 refers to this line
	DataStructure fourthDataSet = secondDataSet;

	return 0;
	
}
*/