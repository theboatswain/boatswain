import re
import sys

file_to_update = sys.argv[1]

with open(file_to_update, 'r') as myfile:
    data = myfile.read()

version_search = re.search(r'APP_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', data, re.IGNORECASE)

if version_search:
    print(version_search.group(1))
