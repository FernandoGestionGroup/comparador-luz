import brotli
import json

payload = {"ok": True, "data": {"cliente": "Juan Perez"}}
json_str = json.dumps(payload).encode('utf-8')

compressed = brotli.compress(json_str)
print("Brotli starts with:", repr(compressed[:10]))

import gzip
compressed_gz = gzip.compress(json_str)
print("Gzip starts with:", repr(compressed_gz[:10]))
