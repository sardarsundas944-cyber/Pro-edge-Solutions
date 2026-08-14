import os
import subprocess

os.chdir(r'd:\Day 5 Task File Handling & Exception Handling Objective')

for f in ['final_cleanup.py', 'create_test_data.py', 'cleanup.py']:
    try:
        if os.path.exists(f):
            os.remove(f)
    except:
        pass

subprocess.run(['git', 'add', '-A'], capture_output=True)
subprocess.run(['git', 'commit', '-m', 'Remove temporary helper files'], capture_output=True)
subprocess.run(['git', 'push', 'origin', 'master'], capture_output=True)

print("✓ Repository cleanup complete!")
print("\nFinal files in repository:")
result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
for line in result.stdout.strip().split('\n'):
    if line:
        print(f"  ✓ {line}")
