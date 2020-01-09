import re
import sys

file_to_update = sys.argv[1]
version = sys.argv[2]

with open(file_to_update, 'r') as myfile:
    data = myfile.read()

data = re.sub(r'APP_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', 'APP_VERSION = "%s"' % version, data)

with open(file_to_update, 'w') as f:
    f.write(data)
