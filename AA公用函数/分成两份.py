import os


def load_config(filename: str):
    filename = os.path.abspath(filename)
    if os.path.isfile(filename):
        with open(filename) as f:
            lines = f.readlines()
    data = []
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        split = line_strip.split()
        assert len(split) == 2
        src = split[0].strip()
        desc = split[1].strip()
        data.append((src, desc))
    print(f"split info:{data}")
    return data