"""
Constants required by this testbed.
"""

from __future__ import annotations

import enum
import pathlib
import typing

from octoprobe.util_baseclasses import TENTACLE_TYPE_MCU
from octoprobe.util_constants import DIRECTORY_OCTOPROBE_GIT_CACHE

if typing.TYPE_CHECKING:
    from .tentacle_spec import TentacleShowcase


TAG_BUILD_VARIANTS = "build_variants"
TAG_BOARD = "board"

TESTBED_NAME = "testbed_showcase"

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent
DIRECTORY_REPO = DIRECTORY_OF_THIS_FILE.parent.parent
print(DIRECTORY_REPO / "pytest.ini")
assert (DIRECTORY_REPO / "pytest.ini").is_file()
DIRECTORY_DOWNLOADS = DIRECTORY_REPO / "downloads"
DIRECTORY_TESTRESULTS_DEFAULT = DIRECTORY_REPO / "results"
DIRECTORY_GIT_CACHE = DIRECTORY_OCTOPROBE_GIT_CACHE
FILENAME_TESTBED_LOCK = DIRECTORY_REPO / "testbed.lock"


class EnumTentacleType(enum.StrEnum):
    TENTACLE_MCU = TENTACLE_TYPE_MCU
    TENTACLE_DEVICE_POTPOURRY = "potourry"
    TENTACLE_DAQ_SALEAE = "daq_saleae"

    def get_tentacles_for_type(
        self,
        tentacles: list[TentacleShowcase],
        required_futs: list[EnumFut],
    ) -> list[TentacleShowcase]:
        """
        Select all tentacles which correspond to this
        TentacleType and list[EnumFut].
        """

        def has_required_futs(t: TentacleShowcase) -> bool:
            if t.tentacle_spec.tentacle_type == self:
                for required_fut in required_futs:
                    if required_fut in t.tentacle_spec.futs:
                        return True
            return False

        return [t for t in tentacles if has_required_futs(t)]


class EnumFut(enum.StrEnum):
    FUT_MCU_ONLY = enum.auto()
    """
    Do not provide a empty list, use FUT_MCU_ONLY instead!
    """
    FUT_I2C = enum.auto()
    FUT_UART = enum.auto()
    FUT_ONEWIRE = enum.auto()
    FUT_TIMER = enum.auto()
