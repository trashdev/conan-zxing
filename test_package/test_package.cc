#include <stdio.h>
#include <string.h>
#include <zxing/common/StringUtils.h>

int main()
{
	char *text = strdup("Hello world");
	std::string encoding = zxing::common::StringUtils::guessEncoding(text, strlen(text), zxing::common::StringUtils::Hashtable());
	if (encoding != "ISO8859-1")
	{
		fprintf(stderr, "Error initializing ZXing.  Detected %s.\n", encoding.c_str());
		return -1;
	}
	printf("Successfully initialized ZXing.  Detected %s.\n", encoding.c_str());
	return 0;
}
