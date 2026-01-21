import os
import sys
import subprocess

try:
    result = subprocess.run([r'..\venv\Scripts\python', 'manage.py', 'migrate'], 
                            capture_output=True, text=True)
    with open('migrate_log.txt', 'w') as f:
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
except Exception as e:
    with open('migrate_log.txt', 'w') as f:
        f.write("EXCEPTION: " + str(e))
