import argparse
import importlib.util
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=("Tell seastersdb where the database is located.")
    )
    parser.add_argument("path", help="path to the database")
    args = parser.parse_args()

    # Package existence check
    spec = importlib.util.find_spec("seastersdb")
    if not spec:
        sys.stderr.write("Failure: Package `seastersdb` not found.\n")
        sys.stderr.write("Install it then re-run.\n")
        sys.exit(1)
    assert spec.origin is not None

    # Write data directory in 'seastersdb/data/path.txt'
    file = Path(spec.origin).parent / "data" / "path.txt"
    file.write_text(str(Path(args.path).resolve()))
    sys.stdout.write(
        f"API configuration completed! (package location: {Path(spec.origin).parent})\n"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
