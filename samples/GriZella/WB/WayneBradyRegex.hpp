#ifndef WAYNE_BRADY_REGEX_HPP
#define WAYNE_BRADY_REGEX_HPP

#include <boost/regex.hpp>
using boost::regex;

namespace wbregex {
	static const regex reNL("\n+");
	static const regex reClean("[<>&]|[^\\x20-x127\\w\\n+]");
	static const regex reCSV(",(?=([^\"]*\"[^\"]*\")*(?![^\"]*\"))");
	static const regex reTrailingSlash("/$");
	static const regex reQuotes("[\"\']");
	static const regex reComma("[,]");
	static const regex reStripNonNumeric("[^0-9^.]");
	static const regex reCity("[^ ^A-Z^a-z^0-9^-^\\(^\\)^:^;]");
	static const regex reRateAlpha("NEG|CALL", regex::icase);
	static const regex reRateNumeric("[\\$|\\d|\\.|,]+");
	static const regex reStripNonDate("[^0-9/\\s\\-]");
	static const regex reDateYYYYMMDD("(^\\d{4})(\\d{2})(\\d{2})(.*)");
	static const regex reDateMDY("(^\\d{1,2})(/)(\\d{1,2})(/)(\\d{2,4})(.*)");
	static const regex reDateMDYDash("(^\\d{1,2})(-)(\\d{1,2})(-)(\\d{2,4})(.*)");
	static const regex reLeadingZero("^[0]");
	static const regex reStripNonTime("[^0-9^:AaPp]");
	static const regex reTimeHM("(^\\d{1,2})(:)(\\d{2})([aApP]?)(.*)");
	static const regex reComment("[,'`]|[^\\w!$#%)(-:*;]");
	static const regex reAlphaNumeric("[^A-Za-z0-9]");
}

#endif // WAYNE_BRADY_REGEX_HPP
