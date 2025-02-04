import logging

from octoprobe.util_constants import TAG_BOARDS
from octoprobe.util_firmware_spec import FirmwareBuildSpec, FirmwareSpecBase
from octoprobe.util_micropython_boards import BoardVariant, board_variants

from testbed_showcase.tentacle_spec import TentacleShowcase

logger = logging.getLogger(__file__)


_ENV_MICROPY_DIR = "MICROPY_DIR"


def collect_firmware_specs(tentacles: list[TentacleShowcase]) -> list[FirmwareSpecBase]:
    """
    Loops over all tentacles and finds
    the board variants that have to be
    build/downloaded.
    """
    set_variants: set[BoardVariant] = set()
    for tentacle in tentacles:
        if not tentacle.is_mcu:
            continue
        boards = tentacle.get_tag_mandatory(TAG_BOARDS)
        for variant in board_variants(boards):
            set_variants.add(variant)
    list_variants = sorted(set_variants, key=lambda v: v.name_normalized)

    return [FirmwareBuildSpec(board_variant=variant) for variant in list_variants]
