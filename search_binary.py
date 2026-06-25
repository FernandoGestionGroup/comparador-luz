import os

search_prefix = b"1%\xef\xbf\xbdW%7"
search_prefix_fallback = b"1%"

print("Buscando archivos que comiencen con 1%...")

for root, dirs, files in os.walk("."):
    if ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        path = os.path.join(root, f)
        try:
            with open(path, "rb") as fd:
                header = fd.read(10)
                if header.startswith(b"1%"):
                    print(f"MATCH (1%): {path} -> {header.hex()}")
        except Exception:
            pass
