from collections.abc import Sequence

import pandas as pd

from structs.match import Match
from structs.oponents import Scenario
from structs.rand_oponents import RandAdversary
from structs.spirit import Spirit


class Datasets:
    adversaries: pd.DataFrame
    games: pd.DataFrame
    scenarios: pd.DataFrame
    sets: pd.DataFrame
    spirits: pd.DataFrame

    def __init__ (self) -> None:
        self._load_datasets()

    def _load_datasets (self) -> None:
        self.adversaries = pd.read_csv("content/adversaries.csv")
        self.sets = pd.read_csv("content/sets.csv")
        self.games = pd.read_csv("content/games.csv")
        self.scenarios = pd.read_csv("content/scenarios.csv")
        self.spirits = pd.read_csv("content/spirits.csv")

    def get_spirit_name (self, spirit_id: str) -> str:
        return self.spirits[self.spirits.id == spirit_id].iloc[0].spirit

    def get_adversary_name (self, adversary_id: str) -> str:
        return self.adversaries[self.adversaries.id == adversary_id].iloc[0].adversary

    def save_game (
        self, spirits: list[str], win: bool, solo: bool = True, score: int = -1,
        adversaries: list[str] = (), scenario: str | None = None, archipelago: bool = False
    ) -> None:
        if len(self.spirits[self.spirits.id.isin(spirits)]) != len(spirits):
            raise ValueError("Invalid spirit id")

        if len(self.adversaries[self.adversaries.id.isin(adversaries)]) != len(adversaries):
            raise ValueError("Invalid adversary id")

        if scenario is not None and len(self.scenarios[self.scenarios.id == scenario]) != 1:
            raise ValueError("Invalid scenario id")

        spirits = sorted(spirits)
        adversaries = sorted(adversaries)

        entry = pd.DataFrame([{
            "solo": solo,
            "spirits": ",".join(spirits),
            "adversaries": ",".join(adversaries),
            "scenario": scenario,
            "win": win,
            "score": score,
            "archipelago": archipelago,
        }])

        self.games = pd.concat((self.games, entry), ignore_index=True)
        self.games.to_csv("content/games.csv", index=False)

    def random_game (
        self, n_spirits: int = 1, n_adversaries: int = 1,
        with_scenario: bool = False,
        with_aspects: bool = False,
        ignored_spirits: Sequence[str] = (),
        ignored_adversaries: Sequence[str] = (),
        ignored_scenarios: Sequence[str] = (),
    ) -> Match:
        owned_sets = self.sets[self.sets["own"]]["set"]

        owned_spirits = self.spirits[
            self.spirits["set"].isin(owned_sets)
            & ~self.spirits["spirit"].isin(ignored_spirits)
        ]
        if not with_aspects:
            owned_spirits = owned_spirits[owned_spirits["aspect"].isna()]

        owned_adversaries = self.adversaries[
            self.adversaries["set"].isin(owned_sets)
            & ~self.adversaries["adversary"].isin(ignored_adversaries)
        ]

        owned_scenarios = self.scenarios[
            self.scenarios["set"].isin(owned_sets)
            & ~self.scenarios["scenario"].isin(ignored_scenarios)
        ]

        chosen_spirits = [
            Spirit.from_sample(row)
            for _, row in owned_spirits.sample(n_spirits).iterrows()
        ]
        chosen_adversaries = [
            RandAdversary.from_sample(row, lvls=(0, 1, 2, 3, 4, 5, 6))
            for _, row in owned_adversaries.sample(n_adversaries).iterrows()
        ]

        chosen_scenario = None
        if with_scenario:
            chosen_scenario = Scenario.from_sample(owned_scenarios.sample(1).iloc[0])

        return Match(
            spirits=chosen_spirits,
            adversaries=chosen_adversaries,
            scenario=chosen_scenario
        )

    def filter_spirits_games (self, spirits: Sequence[str] = ()) -> pd.DataFrame:
        if len(spirits) == 0:
            return pd.DataFrame([], columns=self.games.columns)

        spirits = sorted(spirits)

        return self.games[
            self.games.spirits.str.contains(".*".join(spirits), regex=True)
        ]

    def filter_adversaries_games (self, adversaries: Sequence[str] = ()) -> pd.DataFrame:
        if len(adversaries) == 0:
            return pd.DataFrame([], columns=self.games.columns)

        adversaries = sorted(adversaries)

        return self.games[
            self.games.adversaries.str.contains(".*".join(adversaries), regex=True)
        ]

    def filter_scenario_games (self, scenario: str) -> pd.DataFrame:
        return self.games[self.games.scenario == scenario]
