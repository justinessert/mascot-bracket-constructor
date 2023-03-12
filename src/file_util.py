import os
import yaml
import pandas as pd
import json
import sys

sys.path.insert(0, "..")

from src.const import REGIONS, DATA_DIR  # noqa: E402


def safe_load_yaml(filepath):
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def safe_loads(s):
    try:
        return json.loads(s.replace("'", '"'))
    except json.JSONDecodeError:
        return s


def load_data(region, rnd, year="2023"):
    if rnd < 5:
        df = pd.read_csv(os.path.join(DATA_DIR, year, f"{region}_{rnd}.csv"))
    elif rnd == 5:
        df = pd.concat(
            [
                pd.read_csv(os.path.join(DATA_DIR, year, f"{r}_{rnd}.csv"))
                for r in REGIONS
            ]
        )
    elif rnd == 6:
        df = pd.read_csv(os.path.join(DATA_DIR, year, "final.csv"))
    else:
        df = pd.read_csv(os.path.join(DATA_DIR, year, "champion.csv"))

    df = df.set_index("effective_seed")
    df["team_name"] = df["team_name"].map(lambda x: safe_loads(x))
    return df


def save_data(df, region, rnd, year="2023"):
    if rnd < 6:
        df.to_csv(os.path.join(DATA_DIR, year, f"{region}_{rnd}.csv"))
    elif rnd == 6:
        df.to_csv(os.path.join(DATA_DIR, year, "final.csv"))
    else:
        df.to_csv(os.path.join(DATA_DIR, year, "champion.csv"))
