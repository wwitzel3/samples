#ifndef WAYNE_BRADY_VALIDATORS_HPP
#define WAYNE_BRADY_VALIDATORS_HPP

#include <string>
#include <map>
using std::string;
using std::map;
using std::pair;

#include "WayneBradyRegex.hpp"

namespace wbvalidators {
	typedef string(*validator)(string&, string);
	typedef map<string, pair<validator, string> > validator_map;
};

wbvalidators::validator_map* generate_map(bool isLoads);

#endif // WAYNE_BRADY_VALIDATORS_HPP
