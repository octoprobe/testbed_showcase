from __future__ import annotations

import dataclasses

from octoprobe import util_mcu_pico, util_mcu_pyboard

from testbed_showcase.constants import EnumFut, EnumTentacleType

from .tentacle_spec import TentacleSpecShowcase


@dataclasses.dataclass
class McuConfig:
    """
    These variables will be replaced in micropython code
    """

    # Used in jinja2 templates to generate micropython code
    trig1: str
    trig2: str
    data1: str
    data2: str
    i2c: str
    onewire: str

    # Used elsewere
    micropython_perftest_args: list[str] | None = None

    def __post_init__(self) -> None:
        assert isinstance(self.trig1, str)
        assert isinstance(self.trig2, str)
        assert isinstance(self.data1, str)
        assert isinstance(self.data2, str)
        assert isinstance(self.i2c, str)
        assert isinstance(self.onewire, str)
        assert isinstance(self.micropython_perftest_args, list | None)


DOC_TENTACLE_PYBV11 = """
See: https://github.com/octoprobe/testbed_showcase/tree/main/docs/tentacle_MCU_PYBV11
"""
MCU_PYBV11 = TentacleSpecShowcase(
    tentacle_type=EnumTentacleType.TENTACLE_MCU,
    tentacle_tag="MCU_PYBV11",
    futs=[
        EnumFut.FUT_MCU_ONLY,
        EnumFut.FUT_I2C,
        EnumFut.FUT_UART,
        EnumFut.FUT_ONEWIRE,
        EnumFut.FUT_TIMER,
    ],
    doc=DOC_TENTACLE_PYBV11,
    mcu_usb_id=util_mcu_pyboard.PYBOARD_USB_ID,
    tags="boards=PYBV11:PYBV11-DP:PYBV11-THREAD:PYBV11-DP_THREAD,mcu=stm32,programmer=dfu-util",
    relays_closed={
        EnumFut.FUT_MCU_ONLY: [],
        EnumFut.FUT_I2C: [2, 3, 4, 5],
        EnumFut.FUT_ONEWIRE: [2, 3, 4],
    },
    mcu_config=McuConfig(
        trig1="Y2",
        trig2="Y3",
        data1="Y9",
        data2="Y10",
        i2c="i2c = I2C(scl='Y9', sda='Y10', freq=100000)",
        onewire="Y9",
    ),
)


DOC_TENTACLE_RPI_PICO = """
See: https://github.com/octoprobe/testbed_showcase/tree/main/docs/tentacle_MCU_RPI_PICO
"""
MCU_RPI_PICO = TentacleSpecShowcase(
    tentacle_type=EnumTentacleType.TENTACLE_MCU,
    tentacle_tag="MCU_RPI_PICO",
    futs=[
        EnumFut.FUT_MCU_ONLY,
        EnumFut.FUT_I2C,
        EnumFut.FUT_UART,
        EnumFut.FUT_ONEWIRE,
        EnumFut.FUT_TIMER,
    ],
    doc=DOC_TENTACLE_RPI_PICO,
    mcu_usb_id=util_mcu_pico.RPI_PICO_USB_ID,
    tags="boards=RPI_PICO,mcu=rp2,programmer=picotool",
    relays_closed={
        EnumFut.FUT_MCU_ONLY: [],
        EnumFut.FUT_I2C: [2, 3, 4, 5],
        EnumFut.FUT_ONEWIRE: [2, 3, 4],
    },
    mcu_config=McuConfig(
        trig1="GP20",
        trig2="GP21",
        data1="GP19",
        data2="GP18",
        i2c="i2c = I2C(1, scl=Pin('GP19'), sda=Pin('GP18'), freq=100_000)",
        onewire="GP14",
    ),
)

MCU_RPI_PICO_W = dataclasses.replace(
    MCU_RPI_PICO,
    tentacle_tag="MCU_RPI_PICO_W",
    tags="boards=RPI_PICO_W,mcu=rp2,programmer=picotool",
)

DOC_TENTACLE_RPI_PICO2 = """
See: https://github.com/octoprobe/testbed_showcase/tree/main/docs/tentacle_MCU_RPI_PICO
"""
MCU_RPI_PICO2 = TentacleSpecShowcase(
    tentacle_type=EnumTentacleType.TENTACLE_MCU,
    tentacle_tag="MCU_RPI_PICO2",
    futs=[
        EnumFut.FUT_MCU_ONLY,
        EnumFut.FUT_I2C,
        EnumFut.FUT_UART,
        EnumFut.FUT_ONEWIRE,
        EnumFut.FUT_TIMER,
    ],
    doc=DOC_TENTACLE_RPI_PICO2,
    mcu_usb_id=util_mcu_pico.RPI_PICO2_USB_ID,
    tags="boards=RPI_PICO2:RPI_PICO2-RISCV,mcu=rp2,programmer=picotool",
    relays_closed={
        EnumFut.FUT_MCU_ONLY: [],
        EnumFut.FUT_I2C: [2, 3, 4, 5],
        EnumFut.FUT_ONEWIRE: [2, 3, 4],
    },
    mcu_config=McuConfig(
        trig1="GP20",
        trig2="GP21",
        data1="GP19",
        data2="GP18",
        i2c="i2c = I2C(1, scl=Pin('GP19'), sda=Pin('GP18'), freq=100_000)",
        onewire="GP14",
    ),
)


DOC_TENTACLE_DEVICE_POTPOURRY = """
FT232RL
  https://www.aliexpress.com/item/1005006445462581.html
I2C EEPROM AT24C08
  https://www.aliexpress.com/item/1005005344566156.html
1Wire Temperature Sensor DS18B20 TO-92
  https://www.aliexpress.com/item/1005004987470850.html
"""
DEVICE_POTPOURRY = TentacleSpecShowcase(
    tentacle_type=EnumTentacleType.TENTACLE_DEVICE_POTPOURRY,
    tentacle_tag="DEVICE_POTPOURRY",
    futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART, EnumFut.FUT_ONEWIRE, EnumFut.FUT_TIMER],
    doc=DOC_TENTACLE_DEVICE_POTPOURRY,
    tags="",
    relays_closed={
        EnumFut.FUT_I2C: [1, 2],
        EnumFut.FUT_ONEWIRE: [5],
    },
)

DOC_TENTACLE_DAQ_SALEAE = """
USB Logic Analyzer 24MHz 8 Channel
https://www.aliexpress.com/item/4000146595503.html
https://sigrok.org/wiki/Noname_Saleae_Logic_clone
"""
DAQ_SALEAE = TentacleSpecShowcase(
    tentacle_type=EnumTentacleType.TENTACLE_DAQ_SALEAE,
    tentacle_tag="DAQ_SALEAE",
    futs=[
        EnumFut.FUT_I2C,
        EnumFut.FUT_UART,
        EnumFut.FUT_ONEWIRE,
        EnumFut.FUT_TIMER,
    ],
    doc=DOC_TENTACLE_DAQ_SALEAE,
    tags="daq=saleae_clone",
    relays_closed={
        EnumFut.FUT_I2C: [1, 2, 3, 4],
        EnumFut.FUT_ONEWIRE: [1, 2, 3, 4],
    },
)
