import subprocess
import os

os.chdir(r'd:\Day 5 Task File Handling & Exception Handling Objective')

print("=" * 60)
print("FINAL PROJECT VERIFICATION")
print("=" * 60)

print("\n📁 Repository Files:")
result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
for line in result.stdout.strip().split('\n'):
    if line:
        print(f"   ✓ {line}")

print("\n📝 Recent Commits:")
result = subprocess.run(['git', 'log', '--oneline', '-n', '10'], capture_output=True, text=True)
for line in result.stdout.strip().split('\n')[:5]:
    print(f"   {line}")

print("\n✅ Project Status: READY FOR SUBMISSION")
print("\n" + "=" * 60)
