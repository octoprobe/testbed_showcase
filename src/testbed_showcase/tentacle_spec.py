from __future__ import annotations

import dataclasses
import typing

from octoprobe.lib_tentacle import TentacleBase
from octoprobe.util_baseclasses import TentacleSpecBase
from octoprobe.util_constants import TAG_MCU

from .constants import TAG_BOARD, TAG_BUILD_VARIANTS

if typing.TYPE_CHECKING:
    from .tentacle_specs import McuConfig


@dataclasses.dataclass(frozen=True, repr=True, eq=True, order=True)
class TentacleSpecShowcase(TentacleSpecBase):
    mcu_config: McuConfig | None = None

    @property
    def micropython_board(self) -> str:
        """
        If
          tags="board=ESP8266_GENERIC, ..."
        is defined, it will be used.
        Fallback to 'tentacle_tag'.
        """
        board = self.get_tag(TAG_BOARD)
        if board is not None:
            return board
        return self.tentacle_tag

    @property
    def description(self) -> str:
        mcu = self.get_tag(TAG_MCU)
        if mcu is None:
            return self.micropython_board
        return mcu + "/" + self.micropython_board

    @property
    def build_variants(self) -> list[str]:
        """
        Example for RP2_PICO: ["", "RISCV"]
        Example for ESP8266_GENERIC: [""]
        """
        variants = self.get_tag(TAG_BUILD_VARIANTS)
        if variants is None:
            return [""]
        return variants.split(":")


class TentacleShowcase(TentacleBase):
    @property
    @typing.override
    def pytest_id(self) -> str:
        """
        Example: 1831-pico2(RPI_PICO2-RISCV)
        Example: 1331-daq
        """
        name = self.label_short
        if self.is_mcu:
            if self.tentacle_state.firmware_spec is None:
                name += "(no-flashing)"
            else:
                name += f"({self.tentacle_state.firmware_spec.board_variant.name_normalized})"
        return name

    @property
    def tentacle_spec(self) -> TentacleSpecShowcase:
        """
        Just does typcasting from TentacleSpecBase to TentacleSpecShowcase
        """
        tentacle_spec_base = self.tentacle_spec_base
        assert isinstance(tentacle_spec_base, TentacleSpecShowcase)
        return tentacle_spec_base
