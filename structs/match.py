import dataclasses as dc

from .oponents import InterfaceAdversary, Scenario
from .spirit import Spirit


@dc.dataclass
class Match:
    spirits: list[Spirit]
    adversaries: list[InterfaceAdversary] = dc.field(default_factory=list)
    scenario: Scenario | None = None

    @property
    def n_spirits (self) -> int:
        return len(self.spirits)

    @property
    def n_adversaries (self) -> int:
        return len(self.adversaries)
