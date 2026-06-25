import sys
import string

signature = b"1%\xef\xbf\xbdW%7\xef\xbf\xbd\xef\xbf\xbd[\xef\xbf\xbd\\\xdb\xb9\xef\xbf\xbd\xef\xbf\xbdR."

# Let's search if this is a known signature
# We know pdf is %PDF, 
# zip is PK
# gzip is 1f 8b
# bzip2 is BZh
# 7z is 37 7a bc af 27 1c
# rar is 52 61 72 21 1a 07

print(signature.hex())
