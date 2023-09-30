import sys
import os

path = sys.argv[1]

os.chdir(path)
diff = os.popen('git diff').readlines()

if not diff[10].startswith('+> Report generated on') and not diff[8].startswith('-> Report generated on'):
  print('true')
else:
  print('false')
