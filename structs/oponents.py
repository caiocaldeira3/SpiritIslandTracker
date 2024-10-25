import dataclasses as dc
from abc import abstractmethod
from typing import Any, Self


@dc.dataclass
class Oponent:
    name: str
    difficulty: int
    img_url: str

@dc.dataclass
class InterfaceAdversary:
    @abstractmethod
    def from_sample (cls, sample: dict[str, Any], lvl: int) -> Self:
        pass

@dc.dataclass
class Adversary (Oponent, InterfaceAdversary):
    lvl: int
    desc: str = "adversary"

    @classmethod
    def from_sample (cls, sample: dict[str, Any], lvl: int) -> Self:
        return cls(
            name=sample["adversary"],
            img_url=sample["img"],
            difficulty=sample[f"dificulty_level_{lvl}"],
            lvl=lvl,
        )

@dc.dataclass
class Scenario (Oponent):
    desc: str = "scenario"

    @classmethod
    def from_sample (cls, sample: dict[str, Any]) -> Self:
        return cls(
            name=sample["scenario"],
            img_url=sample["img"],
            difficulty=sample["difficulty"]
        )
