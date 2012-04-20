// Copyright GriZella, Corp. 2006-2007
// All rights reserved

#include "../include/stdafx.h"
#include "time.h"
#include <string>
#include <map>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <iomanip>

#include <iostream>
using std::cout;
using std::endl;

#include <boost/regex.hpp>

#include "WayneBradyShow.h"
#include "WayneBradyRegex.hpp"
#include "WayneBradyValidators.hpp"
#include "WayneBradyStateMap.hpp"
#include "WayneBradyTruckTypeMap.hpp"

namespace wbvalidators {
	using namespace boost;
	using namespace std;

	typedef string(*validator)(string&, string);
	typedef map<string, pair<validator, string > > validator_map;
	
	static string return_field(string& field, string def="") {
		string s(field);
		return s;
	}

	static string format_numeric(string& field, string def="") {
		// string empty? return the default
		if (field.length() == 0)
			return def;
		else if (field.length() > 4)
			throw WayneBradyShowException("<error>value too large - FN</error>");

		string stor; stor.reserve(field.size()); string r="";
		regex_replace(back_inserter(stor), field.begin(), field.end(), wbregex::reStripNonNumeric, r);

		// no need to continue, no valid numerics in the field
		if (stor.length() == 0)
			return def;

		// convert to int, cutting off percision
		unsigned i;
		istringstream iss(stor);
		iss >> dec >> i;

		// convert back to string
		ostringstream oss;
		oss << i;
		stor = oss.str();

		return stor;
	}

	static string format_numeric_zero_to_one(string& field, string def="") {
		if (field.length() == 0)
			return def;
		else if (field.length() > 4)
			throw WayneBradyShowException("<error>value too large - FNZTO</error>");

		string stor = format_numeric(field, def);
		int i = atoi(stor.c_str());
		if(i==0) stor = "1";
		return stor;
	}

	static string full_partial(string& field, string def="") {
		if (field.length() == 0)
			return def;

		string stor; stor.reserve(field.size());

		std::transform(field.begin(), field.end(), back_inserter(stor), (int(*)(int))std::tolower);

		
		if (!(stor.find("f") == string::npos) || (stor == "tl"))
			stor = "Full";
		else if (!(stor.find("p") == string::npos) || (stor == "ltl"))
			stor = "Partial";
		else
			stor = def;
		
		return stor;
	}

	static string format_numeric_zero_to_blank(string& field, string def="") {
		if (field.length() == 0)
			return def;
		else if (field.length() > 4)
			throw WayneBradyShowException("<error>value too large - FNZTB</error>");

		string stor = format_numeric(field, def);
		int i = atoi(stor.c_str());
		if(i==0) stor = "";
		return stor;
	}

	static string format_weight(string& field, string def="") {
		if (field.length() == 0)
			return def;

 		string stor; stor.reserve(field.size()); string r="";
		regex_replace(back_inserter(stor), field.begin(), field.end(), wbregex::reStripNonNumeric, r);
		
		unsigned iWeight;
		istringstream iss(stor);
		iss >> dec >> iWeight;

		if (iWeight > 999)
			iWeight = iWeight / 1000;

		ostringstream oss;
		oss << iWeight;
		stor = oss.str();

		return stor;
	}

	static string format_rate(string& field, string def="") {
		if (field.length() == 0)
			return def;

		string copy; copy.reserve(field.size());
		regex_replace(back_inserter(copy), field.begin(), field.end(), regex("\\$"), "");
		field = copy;
		
		smatch match; string stor; stor.reserve(field.size());
		if (regex_match(field, match, wbregex::reRateAlpha)) {
			stor = match[0];
			transform(stor.begin(), stor.end(), stor.begin(), (int(*)(int))std::toupper);
			return stor;
		}
		else if (regex_match(field, match, wbregex::reRateNumeric)) {
			stor = match[0];
			string copy; copy.reserve(stor.size());
			regex_replace(back_inserter(copy), stor.begin(), stor.end(), regex(","), "");
			float f;
			istringstream iss(copy);
			iss >> dec >> f;

			ostringstream oss;
			oss << fixed << setprecision(2) << f;
			copy = oss.str();

			return copy;
		}
		else
			return def;
	}

	static string format_city(string& field, string def="") {
		string stor; stor.reserve(field.size());
		if (def == "notEmpty") {
			if (field.length() == 0)
				throw WayneBradyShowException("<error>empty city</error>");
		}
		
		if (field.length() == 0)
			return stor;
		else if (field.length() > 64)
			throw WayneBradyShowException("<error>city too long</error>");
		
		string r="";
               	regex_replace(back_inserter(stor), field.begin(), field.end(), wbregex::reCity, r);

		if (stor.length() == 0)
			throw WayneBradyShowException("<error>city contained no valid characters</error>");
		return stor;
	}

	static string format_city_allow_empty(string& field, string def="") {
		string stor; stor.reserve(field.size());
		if (field.length() == 0)
			return def;
		
		if (field.length() == 0)
			return stor;
		else if (field.length() > 64)
			throw WayneBradyShowException("<error>city too long</error>");
		
		string r="";
               	regex_replace(back_inserter(stor), field.begin(), field.end(), wbregex::reCity, r);

		if (stor.length() == 0)
			throw WayneBradyShowException("<error>city contained no valid characters</error>");
		return stor;
	}

	static string format_state(string& field, string def="") {
		if (field.length() == 0)
			throw WayneBradyShowException("<error>empty state</error>");
		else if (field.length() == 1)
			throw WayneBradyShowException("<error>invalid state</error>");

		string stor = field;
		transform(stor.begin(), stor.end(), stor.begin(), (int(*)(int))std::toupper);
		
		map<string, string>* state_map = new map<string,string>(state_pairs, state_pairs + sizeof (state_pairs) / sizeof(state_pairs[0]));
		map<string,string>::const_iterator citer = state_map->find(stor);
		if (citer == state_map->end()) {
			delete state_map;
			throw WayneBradyShowException("<error>invalid state</error>");
		}
		else {
			stor = citer->second;
			delete state_map;
		}

		return stor;
	}

	static string format_state_allow_empty(string& field, string def="") {
		if (field.length() == 0)
			return def;
		else if (field.length() == 1)
			throw WayneBradyShowException("<error>invalid state</error>");

		string stor = field;
		transform(stor.begin(), stor.end(), stor.begin(), (int(*)(int))std::toupper);
		
		map<string, string>* state_map = new map<string,string>(state_pairs, state_pairs + sizeof (state_pairs) / sizeof(state_pairs[0]));
		map<string,string>::const_iterator citer = state_map->find(stor);
		if (citer == state_map->end()) {
			delete state_map;
			throw WayneBradyShowException("<error>invalid state</error>");
		}
		else {
			stor = citer->second;
			delete state_map;
		}

		return stor;
	}

	static string format_date(string& field, string def="") {
		// The default format for pe that we convert to is m/d/Y
		string stor; stor.reserve(field.size());
		if (def == "notEmpty") {
			if (field.length() == 0)
				throw WayneBradyShowException("<error>empty date</error>");
			else if (field.length() < 6)
				throw WayneBradyShowException("<error>invalid date (need min 6 char)</error>");
		}
		else if (field.length() == 0) {
			return stor;
		}
		string r="";
		regex_replace(back_inserter(stor), field.begin(), field.end(), wbregex::reStripNonDate, r);
		smatch match;
		string month, day, year, formattedDate;
		if(regex_match(stor, match, wbregex::reDateYYYYMMDD)) {
			day = match[3];
			month = match[2];
			year = match[1];
		}
		else if(regex_match(stor, match, wbregex::reDateMDY)) {
			day = match[3];
			month = match[1];
			year = match[5];
		}
		else if(regex_match(stor, match, wbregex::reDateMDYDash)) {
			day = match[3];
			month = match[1];
			year = match[5];
		}
		else throw WayneBradyShowException("<error>invalid date</error>");
		time_t rawTime;
		struct tm* timeInfo;
		time(&rawTime);
		timeInfo = localtime(&rawTime);
		int iDay = atoi(day.c_str());
		int iMonth = atoi(month.c_str());
		int iYear = atoi(year.c_str());
		int nowYear = timeInfo->tm_year+1900;
		// if we got a little year like 07 convert it to 2007
		if((nowYear-iYear)>100) iYear += 2000; // TODO: Y3K bug
		if(abs(nowYear-iYear)>1) throw WayneBradyShowException("<error>Bad year</error>");
		// is it an old date
		int numeribeticalToday = nowYear*10000+(timeInfo->tm_mon+1)*100+timeInfo->tm_mday;
		int numeribeticalDate = iYear*10000+iMonth*100+iDay;
		if(numeribeticalDate<numeribeticalToday) throw WayneBradyShowException("<error>expired date</error>");
		ostringstream oss;
		oss << iMonth << "/" << iDay << "/" << iYear;
		formattedDate = oss.str();

		return formattedDate;
	}

	static string format_time(string& field, string def="") {
		string stor; stor.reserve(field.size());
		if (field.length() == 0) return stor;
		string r="";
		regex_replace(back_inserter(stor), field.begin(), field.end(), wbregex::reStripNonTime, r);
		string hour, minute, ampm, formattedTime;
		smatch match;
		if(regex_match(stor, match, wbregex::reTimeHM)) {
			hour = match[1];
			minute = match[3];
			ampm = match[4];
		}
		else throw WayneBradyShowException("<error>invalid time</error>");
		int iHour = atoi(hour.c_str());
		int iMinute = atoi(minute.c_str());
		if(ampm.size()==0) {
			if(iHour>=12) ampm = "pm";
			else ampm = "am";
		}
		if(ampm.find("a")==0 || ampm.find("A")==0) ampm = "am";
		else if(ampm.find("p")==0 || ampm.find("P")==0) ampm = "pm";
		else ampm = "pm";
		if(iHour>12) iHour -= 12;
		if(iHour>12 || iHour<0) throw WayneBradyShowException("<error>Bad hour</error>");
		if(iMinute>=60 || iMinute<0) throw WayneBradyShowException("<error>Bad minute</error>");

		ostringstream oss;
		oss << iHour << ":";
		oss << setfill('0')  << setw(2) << iMinute;
		oss << ampm;

		formattedTime = oss.str();
		return formattedTime;
	}

	static string format_trucktype(string& field, string def="") {
		if (field.length() == 0)
			throw WayneBradyShowException("<error>empty truckType</error>");
		string stor = field;

		map<string,string>* truck_map = new map<string,string>(trucktype_pairs, trucktype_pairs + sizeof (trucktype_pairs) / sizeof(trucktype_pairs[0]));
		map<string,string>::const_iterator citer = truck_map->find(stor);
		if (citer == truck_map->end()) {
			delete truck_map;
			throw WayneBradyShowException("<error>invalid truckType</error>");
		}
		else {
			stor = citer->second;
			delete truck_map;
		}

		return stor;
	}

	static string format_comment(string& field, string def="") {
		if (field.length() == 0)
			return def;

		string copy; copy.reserve(field.size());
		regex_replace(back_inserter(copy), field.begin(), field.end(), wbregex::reComment, " ");

		copy = copy.substr(0,255);
		return copy;
	}

	static string format_import(string& field, string def="") {
		if (field.length() == 0)
			return def;
		else if (field.length() > 50)
			throw WayneBradyShowException("<error>field too long</error>");

		string copy; copy.reserve(field.size());
		regex_replace(back_inserter(copy), field.begin(), field.end(), wbregex::reAlphaNumeric, " ");

		return copy;
	}

	static string format_destarea(string& field, string def="") {
		if (field.length() == 0)
			return def;
		else if (field.length() > 5)
			throw WayneBradyShowException("<error>field too long</error>");

                string stor; stor.reserve(field.size());
		std::transform(field.begin(), field.end(), back_inserter(stor), (int(*)(int))std::tolower);

                if (!(stor.find("t") == string::npos))
	                stor = "true";
                else if (!(stor.find("f") == string::npos))
	                stor = "false";
                else {
	        	stringstream ss;
			unsigned i;
			istringstream iss(stor);
			iss >> dec >> i;

			if (i == 1)
				stor = "true";
			else if (i == 0)
				stor = "false";
			else
				stor = "false";
		}

		return stor;
	}

};

// generate the usable vmap instance .. don't forget to delete it when you are done.
wbvalidators::validator_map* generate_map(bool isLoads) {
	using namespace wbvalidators;
	validator_map* vmap = new validator_map;

	// Common Fields
	(*vmap)["originCity"] = pair<validator, string>(&format_city, "notEmpty");
	(*vmap)["originState"] = pair<validator, string>(&format_state, "");
	(*vmap)["truckType"] = pair<validator, string>(&format_trucktype,"");
	(*vmap)["fullOrPartial"] = pair<validator, string>(&full_partial,"Full");
	(*vmap)["length"] = pair<validator, string>(&format_numeric,"48");
	(*vmap)["weight"] = pair<validator, string>(&format_weight,"0");
	(*vmap)["quantity"] = pair<validator, string>(&format_numeric_zero_to_one,"1");
	(*vmap)["comment"] = pair<validator, string>(&format_comment,"");

	// Load Fields
	if (isLoads) {
		(*vmap)["destState"] = pair<validator, string>(&format_state,"");
		(*vmap)["destCity"] = pair<validator, string>(&format_city,"");
        (*vmap)["deliveryDate"] = pair<validator, string>(&format_date,"");
		(*vmap)["deliveryTime"] = pair<validator, string>(&format_time,"");
		(*vmap)["pickupDate"] = pair<validator, string>(&format_date,"notEmpty");
		(*vmap)["pickupTime"] = pair<validator, string>(&format_time,"");
		(*vmap)["stops"] = pair<validator, string>(&format_numeric,"0");
		(*vmap)["miles"] = pair<validator, string>(&format_numeric_zero_to_blank,"");
		(*vmap)["rate"] = pair<validator, string>(&format_rate,"");
	}
	// Truck Fields
	else {
		(*vmap)["destState"] = pair<validator, string>(&format_state_allow_empty,"");
		(*vmap)["destCity"] = pair<validator, string>(&format_city_allow_empty,"");
        (*vmap)["destArea"] = pair<validator, string>(&format_destarea,"false");
		(*vmap)["destStateList"] = pair<validator, string>(&return_field,"");
		(*vmap)["destRadius"] = pair<validator, string>(&return_field,"");
		(*vmap)["availDate"] = pair<validator, string>(&format_date,"notEmpty");
		(*vmap)["availTime"] = pair<validator, string>(&format_time,"");
	}

	// Internal fields
	(*vmap)["userDef1"] = pair<validator, string>(&format_comment,"");
	(*vmap)["userDef2"] = pair<validator, string>(&format_comment,"");
	(*vmap)["userDef3"] = pair<validator, string>(&format_comment,"");
	(*vmap)["userDef4"] = pair<validator, string>(&format_comment,"");
	(*vmap)["userDef5"] = pair<validator, string>(&format_comment,"");
	(*vmap)["userDef6"] = pair<validator, string>(&format_comment,"");
	(*vmap)["note"] = pair<validator, string>(&format_comment,"");
	(*vmap)["importRef"] = pair<validator, string>(&format_import,"");
	(*vmap)["importBatch"] = pair<validator, string>(&format_import,"");

	return vmap;
}

