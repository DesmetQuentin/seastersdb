"""
Running this script configures the current directory to be the root data
directory where the PySEASTERS Python package looks at for loading data.

Usage:
    python configure_api.py
"""

import importlib.util
import sys
from pathlib import Path

if __name__ == "__main__":
    # Package existence check
    spec = importlib.util.find_spec("seastersdb")
    if not spec:
        sys.stderr.write("Failure: Package `seastersdb` not found.\n")
        sys.stderr.write("Install it then re-run.\n")
        sys.exit(1)

    # Write data directory in 'seastersdb/data/path.txt'
    file = Path(spec.origin).parent / "data" / "path.txt"
    file.write_text(str(Path(__name__).parent.resolve()))
    sys.stdout.write("API configuration completed!\n")
    sys.exit(0)
