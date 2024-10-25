import dataclasses as dc
from typing import Any, Self


@dc.dataclass
class Spirit:
    name: str
    img_url: str
    aspect: str | None

    @classmethod
    def from_sample (cls, sample: dict[str, Any]) -> Self:
        return cls(
            name=sample["spirit"],
            img_url=sample["img"],
            aspect=sample.get("aspect", None)
        )
