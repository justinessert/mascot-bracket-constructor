import os

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)
NICKNAMES_FILE = os.path.join(DATA_DIR, "nicknames.yml")
REGIONS = ["west", "south", "midwest", "east"]
