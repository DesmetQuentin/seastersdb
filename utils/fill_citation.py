#!/usr/bin/env python3

from pathlib import Path
import yaml

excluded_patterns = [
    "*station_id=ISH/citation/ISH_radiation_2*yaml",
    "*station_id=LYU/citation/LYU_radiation_2*yaml",
    "*station_id=MNM/citation/MNM_radiation_2*yaml",
    "*station_id=YUS/citation/YUS_radiation_2*yaml",
]
base = Path("~/work/data/SEASTERS/BSRN").expanduser()
selected_files = sorted(
    f for f in base.glob("station_id=*/citation/*.yaml")
    if not any(f.match(p) for p in excluded_patterns)
)
output_file = Path("all_citations.txt").expanduser()

with output_file.open("w", encoding="utf-8") as fout:
    for yaml_file in selected_files:
        print(yaml_file)
        with yaml_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        citation = data.get("Citation")
        if citation:
            fout.write(str(citation).strip())
            fout.write("\n")

print(f"Wrote citations to {output_file}")
