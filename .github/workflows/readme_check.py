import sys
import subprocess

path = sys.argv[1]

diff = subprocess.run(
  ['git', 'diff', '--', 'README.md'],
  cwd=path,
  check=True,
  capture_output=True,
  text=True,
).stdout.splitlines()

changed_lines = [
  line[1:]
  for line in diff
  if line.startswith(('+', '-')) and not line.startswith(('+++ ', '--- '))
]

commit_needed = any(
  not line.startswith('> Report generated on')
  for line in changed_lines
)

print(str(commit_needed).lower())
