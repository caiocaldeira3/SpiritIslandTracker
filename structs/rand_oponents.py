import dataclasses as dc
from collections.abc import Sequence
from typing import Any, Self

from .oponents import InterfaceAdversary


@dc.dataclass
class RandAdversary (InterfaceAdversary):
    name: str
    difficulty: Sequence[int]
    lvl: Sequence[int]
    img_url: str
    desc: str = "rand-adversary"

    @classmethod
    def from_sample (cls, sample: dict[str, Any], lvls: Sequence[int]) -> Self:
        return cls(
            name=sample["adversary"],
            img_url=sample["img"],
            difficulty=[sample[f"dificulty_level_{lvl}"] for lvl in lvls],
            lvl=lvls,
        )
