"""Why Not Pangram?
Examine a String, determine if it contains every letter in the
US-ASCII alphabet. This will ignore case and non US-ASCII characters.

>>> getMissingLetters('A quick brown fox jumps over the lazy dog')
''
>>> getMissingLetters('A slow yellow fox crawls under the proactive dog')
'bjkmqz'
>>> getMissingLetters('Lions, and tigers, and bears, oh my!')
'cfjkpquvwxz'
>>> getMissingLetters('')
'abcdefghijklmnopqrstuvwxyz'

"""

import re

from string import ascii_lowercase
letters = set(ascii_lowercase)

def getMissingLetters(input_string):
    input_lower = input_string.lower()
    input_clean = re.sub('[^a-z]','',input_lower)
    missing_list = letters.difference(set(input_clean))
    return ''.join(sorted(missing_list))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
