/*
 *  Birds.cpp
 *  pcdr-test
 *
 *  Created by Wayne Witzel III on 8/3/10.
 *  Copyright 2010 __MyCompanyName__. All rights reserved.
 *
 */

#include <iostream>
#include <vector>
#include <algorithm>

struct World {
	static int windspeed;
	static int temperature;
};
int World::windspeed = 0;
int World::temperature = 0;

class Bird {
public:	
	void move(bool flight) {
		if (can_fly && flight) fly();
		else if (can_hop && !flight) hop();
	}
	
	void total() { std::cout << "The " << name << " moved " << ttl_d << " ft." << std::endl; }
protected:
	virtual void fly()=0;
	virtual void hop()=0;
	std::string name;
	
	unsigned int fly_d;
	unsigned int hop_d;
	unsigned int ttl_d;
	
	int windspeed;
	int temperature;
	
	bool can_fly;
	bool can_hop;
};


class Penguin : public Bird {
public:
	Penguin(bool can_fly, bool can_hop) {
		this->can_fly = can_fly;
		this->can_hop = can_hop;
		this->name = "Penguin";
		this->hop_d = 2;
	}
	void fly() { ; }
	void hop() { ttl_d += hop_d; }
};

class Hawk : public Bird {
public:
	Hawk(bool can_fly, bool can_hop) {
		this->can_fly = can_fly;
		this->can_hop = can_hop;
		this->name = "Hawk";
		this->fly_d = 100;
		this->windspeed = 40;
	}
	void hop() { ; }
	void fly() { if (World::windspeed <= windspeed) { ttl_d += fly_d; } }
};

class Robin : public Bird {
public:
	Robin(bool can_fly, bool can_hop) {
		this->can_fly = can_fly;
		this->can_hop = can_hop;
		this->name = "Robin";
		this->fly_d = 20; this->windspeed = 20;
		this->hop_d = 1; this->temperature = 0;
	}
	void hop() { if (World::temperature >= 0) { ttl_d += hop_d; } }
	void fly() { if (World::windspeed <= windspeed) { ttl_d += fly_d; } }
};

class Crow : public Bird {
public:
	Crow(bool can_fly, bool can_hop) {
		this->can_fly = can_fly;
		this->can_hop = can_hop;
		this->name = "Crow";
		this->fly_d = 30; this->windspeed = 25;
		this->hop_d = 1; this->temperature = 0;
	}
	void hop() { if (World::temperature >= 0) { ttl_d += hop_d; } }
	void fly() { if (World::windspeed <= windspeed) { ttl_d += fly_d; } }
};

void bird_moves(Bird* b) {
	b->move(true);
	b->move(false);
}

int main() {
	std::vector<Bird*> birds;

	Penguin* penguin = new Penguin(false, true);
	birds.push_back(dynamic_cast<Bird*>(penguin));
	
	Hawk* hawk = new Hawk(true, false);
	birds.push_back(dynamic_cast<Bird*>(hawk));
	
	Robin* robin = new Robin(true, true);
	birds.push_back(dynamic_cast<Bird*>(robin));
	
	Crow* crow = new Crow(true, true);
	birds.push_back(dynamic_cast<Bird*>(crow));
	
	World::temperature = 20;
	World::windspeed = 12;
	for_each(birds.begin(), birds.end(), bird_moves);
	
	// alter speeds
	World::temperature = -10;
	World::windspeed = 30;
	for_each(birds.begin(), birds.end(), bird_moves);
	
	
	// print out and cleanup
	typedef std::vector<Bird*>::iterator it;
	
	for (it first=birds.begin(); first != birds.end(); ++first) {
		(*first)->total();
		delete *first;
	}
	
	return 0;
}

