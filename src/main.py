import matplotlib.pyplot as plt
from PIL import Image
from IPython.display import display, clear_output
import pandas as pd
import asyncio
from random import random
import time
from itertools import product
import json

import ipywidgets as widgets
import warnings

warnings.filterwarnings("ignore")

regions = ["west", "south", "midwest", "east"]


def safe_loads(s):
    try:
        return json.loads(s.replace("'", '"'))
    except json.JSONDecodeError:
        return s


def load_data(region, rnd):
    if rnd < 5:
        df = pd.read_csv(f"data/{region}_{rnd}.csv")
    elif rnd == 5:
        df = pd.concat([pd.read_csv(f"data/{r}_{rnd}.csv") for r in regions])
    elif rnd == 6:
        df = pd.read_csv("data/final.csv")
    else:
        df = pd.read_csv("data/champion.csv")

    df = df.set_index("effective_seed")
    df["team_name"] = df["team_name"].map(lambda x: safe_loads(x))
    return df


def save_data(df, region, rnd):
    if rnd < 6:
        df.to_csv(f"data/{region}_{rnd}.csv")
    elif rnd == 6:
        df.to_csv("data/final.csv")
    else:
        df.to_csv("data/champion.csv")


def prettify(s):
    if isinstance(s, list):
        s = str(s)
    return s.upper().replace("_", " ")


def uglify(s):
    return s.lower().replace(" ", "_")


def show_images(teams):
    fig, ax = plt.subplots(1, 2, figsize=(15, 15))

    for i, team in enumerate(teams):
        with open(f"imgs/{team}.jpg", "rb") as f:
            image = Image.open(f)
            ax[i].axis("off")
            ax[i].set_title(prettify(team), size=20)
            ax[i].imshow(image)
    plt.axis("off")
    fig.show()
    plt.show()


def make_buttons(teams):
    button_names = teams + ["Random"]
    options = widgets.ToggleButtons(
        options=[prettify(x) for x in button_names],
    )
    submit = widgets.Button(description="Submit", icon="check")

    display(options)
    display(submit)

    return options, submit


def get_effective_seed(top_seed, region, rnd):
    if rnd != 4:
        return top_seed.name

    return regions.index(region) + 1


def process_random(teams):
    x = random()
    if x < 0.5:
        return teams[0]
    else:
        return teams[1]


def wait_for_change(options, submit):
    future = asyncio.Future()

    def getvalue(change):
        future.set_result(options.value)

    submit.on_click(getvalue)
    return future


async def run_round(rnd):
    if rnd < 5:
        round_regions = regions
    else:
        round_regions = [None]

    for region in round_regions:
        df = load_data(region, rnd)
        next_df = pd.DataFrame()

        if rnd < 5:
            max_seed = 2 ** (5 - rnd)
        elif rnd == 5:
            max_seed = 4
        else:
            max_seed = 2

        for i in range(1, max_seed // 2 + 1):
            top_seed = df.loc[i]
            bot_seed = df.loc[max_seed + 1 - i]

            top_teams = (
                top_seed["team_name"]
                if isinstance(top_seed["team_name"], list)
                else [top_seed["team_name"]]
            )
            bot_teams = (
                bot_seed["team_name"]
                if isinstance(bot_seed["team_name"], list)
                else [bot_seed["team_name"]]
            )

            winners = []
            for top_team, bot_team in product(top_teams, bot_teams):

                teams = [top_team, bot_team]

                show_images(teams)
                options, submit = make_buttons(teams)

                choice = await wait_for_change(options, submit)
                print(choice)

                if choice == prettify("Random"):
                    winner = process_random(teams)
                    print(f"Selected: {winner}")
                    time.sleep(4)
                else:
                    winner = choice

                time.sleep(1)

                winners.append(winner)

            if len(set(winners)) == 1:
                winners = uglify(winners[0])
            else:
                winners = [uglify(x) for x in winners]

            clear_output()

            effective_seed = get_effective_seed(top_seed, region, rnd)
            winner_df = pd.DataFrame(
                {
                    "team_name": [winners],
                    "seed": top_seed["seed"]
                    if prettify(top_seed["team_name"]) == winner
                    else bot_seed["seed"],
                    "effective_seed": effective_seed,
                    "region": region,
                    "round": rnd + 1,
                }
            )

            next_df = pd.concat([next_df, winner_df])

        save_data(next_df, region, rnd + 1)
        print(f"Done with region: {region}, round: {rnd}")

    time.sleep(10)
