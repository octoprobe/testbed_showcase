from __future__ import annotations

import dataclasses
import logging
import pathlib

from testbed_showcase.constants import EnumTentacleType

from .tentacle_spec import TentacleShowcase

logger = logging.getLogger(__file__)

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent


@dataclasses.dataclass
class Testbed:
    """
    A minimal testbed just contains tentacles.
    However, it might also include usb-hubs, wlan-accesspoints, etc.
    """

    workspace: str
    tentacles: list[TentacleShowcase]

    def __post_init__(self) -> None:
        assert isinstance(self.tentacles, list)
        for tentacle in self.tentacles:
            assert isinstance(tentacle, TentacleShowcase)

    @property
    def description_short(self) -> str:
        return TentacleShowcase.tentacles_description_short(tentacles=self.tentacles)

    def get_tentacle(
        self, tentacle_type: EnumTentacleType | None = None, serial: str | None = None
    ) -> TentacleShowcase:
        assert isinstance(tentacle_type, EnumTentacleType | None)
        assert isinstance(serial, str | None)

        list_tentacles: list[TentacleShowcase] = []
        for tentacle in self.tentacles:
            if tentacle_type is not None:
                if tentacle_type != tentacle.tentacle_spec_base.tentacle_type:
                    continue
            if serial is not None:
                if serial != tentacle.tentacle_serial_number:
                    continue
            list_tentacles.append(tentacle)

        line_criterial = f"Criteria tentacle_type='{tentacle_type}', serial='{serial}'."

        if len(list_tentacles) == 0:
            lines1: list[str] = [
                "No tentacles found.",
                line_criterial,
                "These tenacles are configured:",
                self.description_short,
            ]
            raise ValueError("\n".join(lines1))

        if len(list_tentacles) > 1:
            lines2: list[str] = [
                f"{len(list_tentacles)} tentacles match. Please specify serial.",
                line_criterial,
                "These tenacles are configured and already selected:",
                TentacleShowcase.tentacles_description_short(tentacles=list_tentacles),
            ]
            raise ValueError("\n".join(lines2))

        return list_tentacles[0]
