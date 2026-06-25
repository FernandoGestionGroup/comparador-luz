import sys
import subprocess
import json

subprocess.check_call([sys.executable, "-m", "pip", "install", "brotli", "--quiet"])

import brotli

payload1 = {"ok": True, "data": {"cliente": "Test"}}
json_str1 = json.dumps(payload1).encode('utf-8')

compressed1 = brotli.compress(json_str1)
print("Payload 1 starts with:", repr(compressed1[:10]))

payload2 = {"ok": True, "data": {"cliente": "Another much longer test string with more entropy and data!" * 10}}
json_str2 = json.dumps(payload2).encode('utf-8')

compressed2 = brotli.compress(json_str2)
print("Payload 2 starts with:", repr(compressed2[:10]))
