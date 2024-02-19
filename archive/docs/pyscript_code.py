# flake8: noqa=E266,F821

### IMPORTS ###
import asyncio
import io
from itertools import product
import json
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Optional, Tuple
import yaml
from PIL import Image


from pyodide.http import open_url, pyfetch
from pyodide.ffi import create_proxy


### GLOBALS ###

GH_URL = (
    "https://raw.githubusercontent.com/justinessert/mascot-bracket-constructor/main/"
)

REGIONS = ["west", "south", "midwest", "east"]
REGION_ELEMENTS = js.document.getElementsByName("region")

YEAR = 2023

### Helper Functions ###


def get_nicknames():
    url = f"{GH_URL}data/nicknames.yml"
    nicknames = yaml.safe_load(open_url(url).read())
    return nicknames


def safe_loads(s):
    try:
        return json.loads(s.replace("'", '"'))
    except json.JSONDecodeError:
        return s


def get_max_seed(rnd):
    if rnd < 5:
        max_seed = 2 ** (5 - rnd)
    elif rnd == 5:
        max_seed = 4
    else:
        max_seed = 2
    return max_seed


def prettify(s):
    if isinstance(s, list):
        s = " / ".join(s)
    return s.upper().replace("_", " ")


def clear_choice(msg: str = ""):
    display(msg, target="graph-area", append=False)
    Element("buttons").add_class("hidden")
    Element("team-0").write("")
    Element("team-1").write("")


### Data Classes


class Team:
    def __init__(self, name: str, nickname: str, seed: int, region_name: str):
        self.name: str = name
        self.nickname: str = nickname
        self.seed: int = seed
        self.region_name: str = region_name
        self.image: Image = None

    @property
    def pretty_name_nickname(self) -> str:
        return prettify(f"{self.name} {self.nickname}")

    @property
    def pretty_seed_name(self) -> str:
        return prettify(f"{self.seed} {self.name}")


class EffectiveSeed:
    def __init__(self, effective_seed: int, teams: List[Team]):
        self.effective_seed: int = effective_seed
        self.teams: List[Team] = teams

    @property
    def pretty_name(self):
        return prettify([team.pretty_seed_name for team in self.teams])


class Matchup:
    def __init__(
        self,
        rnd: int,
        region_name: str,
        effective_seed: int,
        top_seed: EffectiveSeed,
        bot_seed: EffectiveSeed,
    ):
        self.rnd: int = rnd
        self.region_name: str = region_name
        self.effective_seed: int = effective_seed
        self._possible_matchups: List[Tuple[Team, Team]] = list(
            product(top_seed.teams, bot_seed.teams)
        )
        self.winners: List[Team] = []

    @property
    def is_complete(self) -> bool:
        return not self._possible_matchups

    async def show(self):
        display("Loading Images...", target="graph-area", append=False)
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        teams = self._possible_matchups[0]

        for i, team in enumerate(teams):
            Element(f"team-{i}").write(team.pretty_name_nickname)
        Element("buttons").remove_class("hidden")

        for i, team in enumerate(teams):
            if team.image is None:
                url = f"{GH_URL}imgs/{team.name}.jpg"

                img = await pyfetch(url)
                res = await img.bytes()
                iobuf = io.BytesIO(res)
                team.image = Image.open(iobuf)

            axes[i].imshow(team.image)
            axes[i].axis("off")
            axes[i].set_title(team.pretty_name_nickname, size=20)

        plt.tight_layout()
        display(fig, target="graph-area", append=False)

    def set_winner(self, winner_idx):
        matchup = self._possible_matchups.pop(0)
        plt.close()
        display(
            f"Selected {matchup[winner_idx].pretty_name_nickname}",
            target="graph-area",
            append=False,
        )
        if matchup[winner_idx] not in self.winners:
            self.winners.append(matchup[winner_idx])


class Round:
    def __init__(self, rnd: int, region_name: str, final_round: bool = False):
        self.rnd: int = rnd
        self.region_name: str = region_name

        self._current_matchup_idx = 1

        self._final_round = final_round
        self._max_seed: int = 1 if final_round else get_max_seed(self.rnd)
        self._seeds: dict = {i: None for i in range(1, self._max_seed + 1)}

        self._max_matchup: int = self._max_seed // 2
        self._matchups: dict = {i: None for i in range(1, self._max_matchup + 1)}

    @property
    def is_ready(self) -> bool:
        return all(self._seeds.values())

    @property
    def is_complete(self) -> bool:
        if not self.is_ready:
            return False

        return all([matchup.is_complete for matchup in self._matchups.values()])

    @property
    def current_matchup(self) -> Matchup:
        if self._current_matchup_idx not in self._matchups:
            display(
                f"Matchup {self._current_matchup_idx} not found in matchups: {self._matchups}",
                target="errors",
                append=False,
            )
        return self._matchups[self._current_matchup_idx]

    def _set_seed_element(self, effective_seed: int, seed: EffectiveSeed):
        if not self._final_round:
            element_name = f"rnd{self.rnd}-eSeed{effective_seed}"
        elif self.region_name in REGIONS:
            element_name = "region-winner"
        else:
            element_name = "champion"
        name = seed.pretty_name if seed is not None else " "
        Element(element_name).write(name)

    def set_bracket(self):
        for effective_seed, seed in self._seeds.items():
            self._set_seed_element(effective_seed, seed)

    def _validate_seeds(self):
        invalid_seeds = [i for i, seed in self._seeds.items() if seed is None]
        if invalid_seeds:
            msg = f"Some seeds are correctly initialized: {invalid_seeds}"
            raise ValueError(msg)

    def _validate_matchups(self):
        invalid_matchups = [i for i, seed in self._matchups.items() if seed is None]
        if invalid_matchups:
            msg = f"Some matchups are correctly initialized: {invalid_matchups}"
            raise ValueError(msg)

    def _initialize_matchups(self):
        self._validate_seeds()

        for matchup_idx in self._matchups.keys():
            top_seed_idx = matchup_idx
            bot_seed_idx = self._max_seed + 1 - top_seed_idx

            self._matchups[matchup_idx] = Matchup(
                rnd=self.rnd,
                region_name=self.region_name,
                effective_seed=matchup_idx,
                top_seed=self._seeds[top_seed_idx],
                bot_seed=self._seeds[bot_seed_idx],
            )

        self._validate_matchups()

    def set_seed(self, effective_seed: int, teams: List[Team]):
        seed = EffectiveSeed(
            effective_seed=effective_seed,
            teams=teams,
        )

        self._seeds[effective_seed] = seed

        self._set_seed_element(effective_seed, seed)

        if self.is_ready:
            self._initialize_matchups()

    def _initialize_teams(self, seed_data: pd.Series, nicknames: dict) -> List[Team]:
        if isinstance(seed_data["team_name"], list):
            teams = [
                Team(
                    name=name,
                    nickname=nicknames[name],
                    seed=seed_data["seed"],
                    region_name=seed_data["region"],
                )
                for name in seed_data["team_name"]
            ]
        else:
            teams = [
                Team(
                    name=seed_data["team_name"],
                    nickname=nicknames[seed_data["team_name"]],
                    seed=seed_data["seed"],
                    region_name=seed_data["region"],
                )
            ]

        return teams

    def initialize_seeds_with_data(self, nicknames: dict):
        url = f"{GH_URL}data/{YEAR}/{self.region_name}_{self.rnd}.csv"
        data = pd.read_csv(open_url(url))

        data["team_name"] = data["team_name"].map(lambda x: safe_loads(x))
        data = data.set_index("effective_seed")

        for seed_idx in data.index.unique():
            teams = self._initialize_teams(
                seed_data=data.loc[seed_idx],
                nicknames=nicknames,
            )
            self.set_seed(effective_seed=seed_idx, teams=teams)

        self._initialize_matchups()

    def set_winner(self, winner_idx: int, next_round):
        self.current_matchup.set_winner(winner_idx)

        if self.current_matchup.is_complete:
            next_round.set_seed(
                effective_seed=self.current_matchup.effective_seed,
                teams=self.current_matchup.winners,
            )
            if self._current_matchup_idx != self._max_matchup:
                self._current_matchup_idx += 1


class Region:
    _min_round = 1
    _max_round = 4
    _initialize_with_data = True

    def __init__(self, region_name: str, nicknames: dict):
        self.region_name: str = region_name

        self._current_round_idx = self._min_round

        rnd_nums = list(range(self._min_round, self._max_round + 1))
        self.rounds = {i: Round(rnd=i, region_name=region_name) for i in rnd_nums}
        self.rounds[self._max_round + 1] = Round(
            rnd=self._max_round + 1, region_name=region_name, final_round=True
        )

        if self._initialize_with_data:
            self.rounds[1].initialize_seeds_with_data(nicknames)

    @property
    def pretty_name(self) -> str:
        return self.region_name.replace("_", " ").title()

    @property
    def current_round(self) -> Round:
        return self.rounds[self._current_round_idx]

    @property
    def next_round(self) -> Round:
        return self.rounds[self._current_round_idx + 1]

    @property
    def current_matchup(self) -> Matchup:
        return self.current_round.current_matchup

    @property
    def region_winner(self) -> Optional[List[Team]]:
        return self.rounds[self._max_round + 1]._seeds[1].teams

    @property
    def is_complete(self):
        return all(
            [
                _round.is_complete
                for i, _round in self.rounds.items()
                if i <= self._max_round
            ]
        )

    def set_bracket(self):
        for _round in self.rounds.values():
            _round.set_bracket()

    def set_winner(self, winner_idx: int):
        self.current_round.set_winner(winner_idx, self.next_round)

        if (
            self.current_round.is_complete
            and self._current_round_idx != self._max_round
        ):
            self._current_round_idx += 1

        if self.is_complete:
            clear_choice(f"Completed {self.pretty_name} Region")

    def show_winner(self):
        clear_choice()
        n_winners = len(self.region_winner)
        fig, axes = plt.subplots(1, n_winners, figsize=(5 * n_winners, 5))
        if n_winners == 1:
            axes = [axes]

        for i, team in enumerate(self.region_winner):
            axes[i].imshow(team.image)
            axes[i].axis("off")
            axes[i].set_title(team.pretty_name_nickname, size=20)

        plt.tight_layout()
        display(fig, target="graph-area", append=False)


class FinalRegion(Region):
    _min_round = 5
    _max_round = 6
    _initialize_with_data = False

    @property
    def is_ready(self) -> bool:
        return self.rounds[self._min_round].is_ready

    def set_seed(self, region: Region):
        if region.is_complete:
            effective_seed = REGIONS.index(region.region_name) + 1

            self.rounds[self._min_round].set_seed(
                effective_seed=effective_seed,
                teams=region.region_winner,
            )


class State:
    def __init__(self, nicknames: dict):
        self.regions = {
            region_name: Region(region_name=region_name, nicknames=nicknames)
            for region_name in REGIONS
        }
        self.regions["final_four"] = FinalRegion(
            region_name="final_four",
            nicknames=nicknames,
        )

        self.current_region = None

    @property
    def final_region(self) -> Region:
        return self.regions["final_four"]

    def set_region(self, region_name):
        clear_choice()
        self.current_region = self.regions[region_name]
        self.current_region.set_bracket()
        self.show_choice()
        return self.current_region.pretty_name

    def show_choice(self):
        if self.current_region.is_complete:
            if self.current_region == self.final_region:
                title = f"Your {YEAR} Champion:"
            else:
                title = f"{self.current_region.pretty_name} Champion:"
            Element("section-title").write(title)
            self.current_region.show_winner()
            return

        if (
            self.current_region == self.final_region
            and self.current_region.current_matchup is None
        ):
            title = "Please Fill Out Other Regions Prior to the Final Four"
            Element("section-title").write(title)
            clear_choice("")
            return

        title = "Which Mascot is Better?"
        Element("section-title").write(title)
        asyncio.ensure_future(self.current_region.current_matchup.show())

    def set_winner(self, winner_idx: int):
        self.current_region.set_winner(winner_idx)

        if self.current_region.is_complete:
            if self.final_region != self.current_region:
                self.final_region.set_seed(self.current_region)

        self.show_choice()


### Initialization Code ###

Element("year").write(YEAR)
nicknames = get_nicknames()
state = State(nicknames)

### Interactive Components ###


def select_region(event):
    for ele in REGION_ELEMENTS:
        if ele.checked:
            current_selected = ele.value
            break

    if current_selected == "final_four":
        Element("regions-bracket").add_class("hidden")
        Element("final-four-bracket").remove_class("hidden")
    else:
        Element("final-four-bracket").add_class("hidden")
        Element("regions-bracket").remove_class("hidden")

    pretty_name = state.set_region(current_selected)
    Element("region_name").write(pretty_name)


ele_proxy = create_proxy(select_region)

for ele in REGION_ELEMENTS:
    if ele.value == "east":
        ele.checked = True
        current_selected = ele.value
        pretty_name = state.set_region(current_selected)
        Element("region_name").write(pretty_name)

    ele.addEventListener("change", ele_proxy)

buttons = [js.document.getElementById(f"button-{i}") for i in range(2)]


def button_0_event(event):
    state.set_winner(0)


function_proxy = create_proxy(button_0_event)
buttons[0].addEventListener("click", function_proxy)


def button_1_event(event):
    state.set_winner(1)


function_proxy = create_proxy(button_1_event)
buttons[1].addEventListener("click", function_proxy)
