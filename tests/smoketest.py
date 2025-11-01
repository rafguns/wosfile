from pathlib import Path

import wosfile

for rec in wosfile.read(Path("data").glob("*.txt")):
    assert type(rec) is dict
