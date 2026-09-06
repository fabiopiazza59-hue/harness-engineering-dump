import subprocess
result = subprocess.run(['python3', 'analysis.py'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)