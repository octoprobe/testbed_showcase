from octoprobe.util_baseclasses import TentaclesCollector

from testbed_showcase.constants import TESTBED_NAME

from . import tentacle_specs

TENTACLES_INVENTORY = (
    TentaclesCollector(testbed_name=TESTBED_NAME)
    .add_testbed_instance(
        testbed_instance="ch_hans_1",
        tentacles=[
            ("e46340474b174429", "v1.0", tentacle_specs.MCU_PYBV11),
            ("e46340474b4e1831", "v1.1", tentacle_specs.MCU_RPI_PICO2),
            ("e46340474b4c1331", "v1.0", tentacle_specs.DAQ_SALEAE),
            ("e46340474b4c3f31", "v1.0", tentacle_specs.DEVICE_POTPOURRY),
        ],
    )
    .add_testbed_instance(
        testbed_instance="ch_hans_2",
        tentacles=[
            ("e46340474b4c2731", "v1.1", tentacle_specs.MCU_RPI_PICO2),
            ("e46340474b283623", "v1.0", tentacle_specs.DAQ_SALEAE),
            ("e46340474b0c3523", "v1.0", tentacle_specs.DEVICE_POTPOURRY),
        ],
    )
    .add_testbed_instance(
        testbed_instance="ch_greenliff_1",
        tentacles=[
            ("e46340474b551722", "v1.0", tentacle_specs.MCU_RPI_PICO),
            ("e46340474b164d29", "v1.0", tentacle_specs.DAQ_SALEAE),
            ("e46340474b574722", "v1.0", tentacle_specs.DEVICE_POTPOURRY),
        ],
    )
    .add_testbed_instance(
        testbed_instance="au_damien_1",
        tentacles=[
            ("e46340474b141c29", "v1.1", tentacle_specs.MCU_RPI_PICO2),
            ("e46340474b121931", "v1.0", tentacle_specs.DAQ_SALEAE),
            ("e46340474b563b21", "v1.0", tentacle_specs.DEVICE_POTPOURRY),
        ],
    )
).inventory
