import copy
import logging
import pathlib
import time
import typing
from collections.abc import Iterator

import pytest
from octoprobe.octoprobe import CtxTestRun
from octoprobe.util_firmware_spec import FirmwareNoFlashingSpec, FirmwareSpecBase
from octoprobe.util_pytest import util_logging
from octoprobe.util_pytest.util_resultdir import ResultsDir
from octoprobe.util_pytest.util_vscode import break_into_debugger_on_exception
from octoprobe.util_pyudev import UdevPoller
from octoprobe.util_testbed_lock import TestbedLock
from pytest import fixture
from testbed_micropython.constants import SUBDIR_MPBUILD
from testbed_micropython.util_firmware_mpbuild_interface import ArgsFirmware

import testbed_showcase.util_testbed
from testbed_showcase.constants import (
    DIRECTORY_GIT_CACHE,
    DIRECTORY_TESTRESULTS_DEFAULT,
    EnumFut,
    EnumTentacleType,
    FILENAME_TESTBED_LOCK,
)
from testbed_showcase.tentacle_spec import TentacleShowcase
from testbed_showcase.util_firmware_specs import (
    DEFAULT_PYTEST_OPT_FIRMWARE,
    PYTEST_OPT_FIRMWARE,
    get_firmware_specs,
)
from testbed_showcase.util_testbed import Testbed, get_testbed

logger = logging.getLogger(__file__)

TESTBED: Testbed | None = None
DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent

DEFAULT_FIRMWARE_SPEC = (
    testbed_showcase.constants.DIRECTORY_REPO
    / "pytest_args_firmware_RPI_PICO2_v1.24.0.json"
)


_TESTBED_LOCK = TestbedLock()

# Uncomment to following line
# to stop tests on exceptions
break_into_debugger_on_exception(globals())


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """
    This is a pytest hook https://docs.pytest.org/en/7.1.x/reference/reference.html?highlight=pytest_generate_tests#std-hook-pytest_generate_tests

    Give a test function like 'test_i2c()' in 'metafunc', this function will create test calls for possible combinations of tentacles and firmware versions.

    Calls `metafunc.parametrize` which defines the tests that have been be collected.

    :param metafunc: See https://docs.pytest.org/en/7.1.x/reference/reference.html#metafunc
    :type metafunc: pytest.Metafunc
    """
    # print(metafunc.definition.nodeid)
    # for marker in metafunc.definition.own_markers:
    #     print(f" {marker!r}")

    assert TESTBED is not None

    def get_marker(name: str) -> pytest.Mark:
        for marker in metafunc.definition.own_markers:
            if marker.name == name:
                return marker
        raise KeyError(f"Marker '{name}' not found!")

    def get_required_futs() -> list[EnumFut]:
        try:
            marker_required_futs = get_marker(name="required_futs")
        except KeyError:
            return []
        assert isinstance(marker_required_futs, pytest.Mark)
        return list(marker_required_futs.args)

    _required_futs = get_required_futs()
    for fut in _required_futs:
        assert EnumFut(fut), fut

    if "mcu" in metafunc.fixturenames:

        def warning(
            firmware_spec: FirmwareSpecBase | None,
            futs: list[EnumFut],
        ) -> None:
            msg = "No tentacles where selected"
            if firmware_spec is not None:
                msg += f" for testing firmware '{firmware_spec.board_variant}'"
            msg += "."
            if len(futs) > 0:
                futs_text = ", ".join(f.name for f in _required_futs)
                msg += f" Required futs: {futs_text}."
            logger.warning(msg)

        list_tentacles: list[TentacleShowcase] = []
        firmware_spec: FirmwareSpecBase = FirmwareNoFlashingSpec.factory()
        for firmware_spec in get_firmware_specs(
            config=metafunc.config,
            tentacles=TESTBED.tentacles,
        ):
            assert isinstance(firmware_spec, FirmwareSpecBase)
            tentacles = EnumTentacleType.TENTACLE_MCU.get_tentacles_for_type(
                tentacles=TESTBED.tentacles,
                required_futs=_required_futs,
            )
            tentacles = list(filter(firmware_spec.match_board, tentacles))
            if len(tentacles) == 0:
                warning(firmware_spec=firmware_spec, futs=_required_futs)
            for tentacle in tentacles:
                # TODO: This might be not required anymore!!!
                # Need to create a copy to the tentacle as we
                # modify it for the test.
                _tentacle = copy.copy(tentacle)
                _tentacle.tentacle_state.firmware_spec = firmware_spec
                list_tentacles.append(tentacle)

        if len(list_tentacles) == 0:
            warning(firmware_spec=firmware_spec, futs=[])
            return
        # print(f"LEN={len(list_tentacles)}")
        metafunc.parametrize("mcu", list_tentacles, ids=lambda t: t.pytest_id)

    if "device_potpourry" in metafunc.fixturenames:
        tentacles = EnumTentacleType.TENTACLE_DEVICE_POTPOURRY.get_tentacles_for_type(
            TESTBED.tentacles,
            required_futs=_required_futs,
        )
        if len(tentacles) == 0:
            return
        assert len(tentacles) > 0
        metafunc.parametrize(
            "device_potpourry",
            tentacles,
            ids=lambda t: t.pytest_id,
        )

    if "daq_saleae" in metafunc.fixturenames:
        tentacles = EnumTentacleType.TENTACLE_DAQ_SALEAE.get_tentacles_for_type(
            TESTBED.tentacles,
            required_futs=_required_futs,
        )
        # assert len(tentacles) > 0
        if len(tentacles) == 0:
            msg = "No TENTACLE_DAQ_SALEAE tentacle was selected. Might be the required FUTS specified for TENTACLE_DAQ_SALEAE"
            raise ValueError(msg)

        metafunc.parametrize(
            "daq_saleae",
            tentacles,
            ids=lambda t: t.pytest_id,
        )


@pytest.fixture
def required_futs(request: pytest.FixtureRequest) -> list[EnumFut]:
    """
    Returns all FUTS (Feature Under Test) which are required
    by the test function referencing this fixture.
    """
    for m in request.node.own_markers:
        assert isinstance(m, pytest.Mark)
        if m.name == "required_futs":
            return list(m.args)
    return []


@pytest.fixture
def active_tentacles(request: pytest.FixtureRequest) -> list[TentacleShowcase]:
    """
    Returns all active tentacles which are required
    by the test function referencing this fixture.
    """

    def inner() -> Iterator[TentacleShowcase]:
        if not hasattr(request.node, "callspec"):
            return
        for _param_name, param_value in request.node.callspec.params.items():
            if isinstance(param_value, TentacleShowcase):
                yield param_value

    return list(inner())


class CtxTestrunShowcase(CtxTestRun):
    def __init__(
        self,
        connected_tentacles: typing.Sequence[TentacleShowcase],
        args_firmware: ArgsFirmware,
    ) -> None:
        assert isinstance(args_firmware, ArgsFirmware)
        super().__init__(connected_tentacles=connected_tentacles)
        self.args_firmware = args_firmware
        self.udev_poller = UdevPoller()

    @typing.override
    def session_teardown(self) -> None:
        self.udev_poller.close()


@fixture(scope="session", autouse=True)
def ctxtestrun(request: pytest.FixtureRequest) -> Iterator[CtxTestrunShowcase]:
    """
    Setup and teardown octoprobe and all connected tentacles.

    Now we loop over all tests an return for every test a `CtxTestRun` structure.
    Using this structure, the test find there tentacles, git-repos etc.
    """
    assert TESTBED is not None

    # TODO: See also: get_firmware_specs()
    # Support: Noflash
    # Support: xy.json
    # Support: git://
    # Support: local directory
    firmware_git_url = request.config.getoption(PYTEST_OPT_FIRMWARE)

    args_firmware = ArgsFirmware(
        firmware_build=firmware_git_url,
        flash_skip=False,
        flash_force=False,
        git_clean=False,
        directory_git_cache=DIRECTORY_GIT_CACHE,
    )
    args_firmware.setup()

    _testrun = CtxTestrunShowcase(
        connected_tentacles=TESTBED.tentacles,
        args_firmware=args_firmware,
    )

    # _testrun.session_powercycle_tentacles()

    yield _testrun

    _testrun.session_teardown()


@fixture(scope="function", autouse=True)
def setup_tentacles(
    ctxtestrun: CtxTestrunShowcase,  # pylint: disable=W0621:redefined-outer-name
    required_futs: tuple[EnumFut],  # pylint: disable=W0621:redefined-outer-name
    active_tentacles: list[TentacleShowcase],  # pylint: disable=W0621:redefined-outer-name
    testresults_directory: ResultsDir,  # pylint: disable=W0621:redefined-outer-name
) -> Iterator[None]:
    """
    Runs setup and teardown for every single test:

    * Setup

      * powercycle the tentacles
      * Turns on the 'active' LED on the tentacles involved
      * Flash firmware
      * Set the relays according to `@pytest.mark.required_futs(EnumFut.FUT_I2C)`.

    * yields to the test function
    * Teardown

      * Resets the relays.

    :param testrun: The structure created by `testrun()`
    :type testrun: CtxTestRun
    """
    if len(active_tentacles) == 0:
        # No tentacle has been specified: This is just a normal pytest.
        # Do not call setup/teardown
        yield
        return

    with util_logging.Logs(testresults_directory.directory_test):
        begin_s = time.monotonic()

        def duration_text(duration_s: float | None = None) -> str:
            if duration_s is None:
                duration_s = time.monotonic() - begin_s
            return f"{duration_s:2.0f}s"

        try:
            logger.info(
                f"TEST SETUP {duration_text(0.0)} {testresults_directory.test_nodeid}"
            )
            mpbuild_artifacts = testresults_directory.directory_top / SUBDIR_MPBUILD
            mpbuild_artifacts.mkdir(parents=True, exist_ok=True)
            for tentacle in active_tentacles:
                ctxtestrun.args_firmware.build_firmware(
                    tentacle=tentacle,
                    mpbuild_artifacts=mpbuild_artifacts,
                )
                ctxtestrun.function_prepare_dut(tentacle=tentacle)
                ctxtestrun.function_setup_infra(
                    udev_poller=ctxtestrun.udev_poller,
                    tentacle=tentacle,
                )
                ctxtestrun.function_setup_dut_flash(
                    udev_poller=ctxtestrun.udev_poller,
                    tentacle=tentacle,
                    directory_logs=mpbuild_artifacts,
                )

            ctxtestrun.setup_relays(futs=required_futs, tentacles=active_tentacles)
            logger.info(
                f"TEST BEGIN {duration_text()} {testresults_directory.test_nodeid}"
            )
            yield

        except Exception as e:
            logger.warning(f"Exception during test: {e!r}")
            logger.exception(e)
            raise
        finally:
            logger.info(
                f"TEST TEARDOWN {duration_text()} {testresults_directory.test_nodeid}"
            )
            try:
                ctxtestrun.function_teardown(active_tentacles=active_tentacles)
            except Exception as e:
                logger.exception(e)
            logger.info(
                f"TEST END {duration_text()} {testresults_directory.test_nodeid}"
            )


@pytest.fixture(scope="function")
def testresults_directory(request: pytest.FixtureRequest) -> ResultsDir:
    """
    Returns the log directory for the test function referencing this fixture.
    """
    return ResultsDir(
        directory_top=DIRECTORY_TESTRESULTS_DEFAULT,
        test_name=request.node.name,
        test_nodeid=request.node.nodeid,
    )


def pytest_sessionstart(session: pytest.Session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    _TESTBED_LOCK.acquire(FILENAME_TESTBED_LOCK)

    global TESTBED  # pylint: disable=W0603:global-statement
    assert TESTBED is None
    TESTBED = get_testbed()


def pytest_sessionfinish(session: pytest.Session):
    global TESTBED
    assert TESTBED is not None
    TESTBED.close()

    _TESTBED_LOCK.unlink()


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    This function name is reserved by pytest.
    See https://docs.pytest.org/en/7.1.x/reference/reference.html#initialization-hooks.

    It will be called to determine the program arguments.

    When calling :code:`pytest --help`, below arguments will be listed!
    """
    parser.addoption(
        PYTEST_OPT_FIRMWARE,
        action="store",
        default=None,
        help=f"The url to a git repo to be cloned and compiled, a path to a source directory. Or a json file with a download location. Syntax: {DEFAULT_PYTEST_OPT_FIRMWARE}.",
    )
