from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parent
projects = [
    ROOT / "10-crispdm-masters-platform",
    ROOT / "11-enterprise-ds-audit",
    ROOT / "12-timepulse-forecasting",
    ROOT / "13-nyc-tlc-mobility-platform",
    ROOT / "14-autogluon-multimodal-suite",
    ROOT / "15-spy-sota-timeseries-alpha",
]

for project in projects:
    print(f"\n=== Tests: {project.name} ===")
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=project, check=True)

print(f"\nAll {len(projects)} replication test suites passed.")
