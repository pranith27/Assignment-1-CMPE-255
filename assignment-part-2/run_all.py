from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).parent
projects=sorted(p for p in ROOT.iterdir() if p.is_dir() and (p/'replication.py').exists())
for p in projects:
    print(f"\n=== {p.name} ===")
    subprocess.run([sys.executable, str(p/'replication.py')], cwd=p, check=True)
print(f"\nCompleted {len(projects)} replications.")
