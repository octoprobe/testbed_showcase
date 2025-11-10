from __future__ import annotations

import dataclasses
import logging
import pathlib
import shutil

from octoprobe.octoprobe import CtxTestRun
from octoprobe.usb_tentacle.usb_tentacle import is_serialdelimtied_valid
from octoprobe.util_pytest import util_logging
from octoprobe.util_pytest.util_logging import Logs

from testbed_showcase.constants import DIRECTORY_TESTRESULTS_DEFAULT, EnumTentacleType
from testbed_showcase.tentacles_inventory import TENTACLES_INVENTORY

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
    logs: Logs

    def __post_init__(self) -> None:
        assert isinstance(self.tentacles, list)
        assert isinstance(self.logs, Logs)
        for tentacle in self.tentacles:
            assert isinstance(tentacle, TentacleShowcase)

    def close(self) -> None:
        self.logs.close()

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


def get_testbed():
    if DIRECTORY_TESTRESULTS_DEFAULT.exists():
        shutil.rmtree(DIRECTORY_TESTRESULTS_DEFAULT, ignore_errors=False)
    DIRECTORY_TESTRESULTS_DEFAULT.mkdir(parents=True, exist_ok=True)

    util_logging.init_logging()
    logs = util_logging.Logs(DIRECTORY_TESTRESULTS_DEFAULT)

    usb_tentacles = CtxTestRun.session_powercycle_tentacles()
    tentacles: list[TentacleShowcase] = []
    for usb_tentacle in usb_tentacles:
        serial_delimited = usb_tentacle.serial_delimited
        assert serial_delimited is not None
        is_serialdelimtied_valid(serial_delimited=serial_delimited)
        try:
            tentacle_instance = TENTACLES_INVENTORY[serial_delimited]
        except KeyError:
            logger.warning(
                f"Tentacle with serial {serial_delimited} is not specified in TENTACLES_INVENTORY."
            )
            continue

        tentacle = TentacleShowcase(
            tentacle_instance=tentacle_instance,
            tentacle_serial_number=serial_delimited,
            usb_tentacle=usb_tentacle,
        )
        tentacles.append(tentacle)

    if len(tentacles) == 0:
        raise ValueError("No tentacles are connected!")

    return Testbed(
        workspace="based-on-connected-boards", tentacles=tentacles, logs=logs
    )
