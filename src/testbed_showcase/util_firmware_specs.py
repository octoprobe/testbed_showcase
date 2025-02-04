import logging
import pathlib

import pytest
from octoprobe.util_firmware_spec import (
    FirmwareBuildSpec,
    FirmwareNoFlashingSpec,
    FirmwareSpecBase,
)
from octoprobe.util_micropython_boards import BoardVariant

from .tentacle_spec import TentacleShowcase

logger = logging.getLogger(__file__)
PYTEST_OPT_FIRMWARE = "--firmware"
PYTEST_OPT_BUILD_MOCK = "MOCK"
DEFAULT_PYTEST_OPT_FIRMWARE = "https://github.com/micropython/micropython.git@master"

# TODO: Is this function obsolete?
def get_firmware_specs(
    config: pytest.Config,
    tentacles: list[TentacleShowcase],
) -> list[FirmwareSpecBase]:
    """
    Given: arguments to pytest, for example PYTEST_OPT_FIRMWARE.
    Now we create firmware specs.
    In case of PYTEST_OPT_FIRMWARE ends with ".json":
      The firmware has to be downloaded.
    In case of PYTEST_OPT_FIRMWARE starts with "git:" or is a direcory:
      The firmware has to be compiled.
    If nothing is specified, we do not flash any firmware: Return None
    """
    assert isinstance(config, pytest.Config)
    assert isinstance(tentacles, list)
    for tentacle in tentacles:
        assert isinstance(tentacle, TentacleShowcase)

    firmware_git_url = config.getoption(PYTEST_OPT_FIRMWARE)
    if firmware_git_url is not None:
        #
        # Collect firmware specs by connected tentacles
        #
        if firmware_git_url == PYTEST_OPT_BUILD_MOCK:
            #
            # Mocked firmware speces
            #
            return [
                FirmwareBuildSpec(
                    BoardVariant.factory("RPI_PICO"),
                    micropython_full_version_text="y",
                    _filename=pathlib.Path("/x/y"),
                ),
                FirmwareBuildSpec(
                    BoardVariant.factory("PYBV11"),
                    micropython_full_version_text="y",
                    _filename=pathlib.Path("/x/y"),
                ),
                FirmwareBuildSpec(
                    BoardVariant.factory("PYBV11-DP"),
                    micropython_full_version_text="y",
                    _filename=pathlib.Path("/x/y"),
                ),
            ]

        from .util_firmware_mpbuild import collect_firmware_specs

        return collect_firmware_specs(tentacles=tentacles)

    #
    # Nothing was specified: We do not flash any firmware
    #
    return [FirmwareNoFlashingSpec.factory()]
