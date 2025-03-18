from octoprobe.util_baseclasses import TentaclesCollector

from testbed_showcase.constants import TESTBED_NAME

from . import tentacle_specs

TENTACLES_INVENTORY = (
    TentaclesCollector(testbed_name=TESTBED_NAME)
    .add_testbed_instance(
        testbed_instance="ch_hans_1",
        tentacles=[
            ("e46340474b17-4429", "v1.0", tentacle_specs.MCU_PYBV11),
            ("e46340474b4e-1831", "v1.1", tentacle_specs.MCU_RPI_PICO2),
            ("e46340474b4c-1331", "v1.0", tentacle_specs.DAQ_SALEAE),
            ("e46340474b4c-3f31", "v1.0", tentacle_specs.DEVICE_POTPOURRY),
            (
                "de646cc20b92-5425",
                "v1.0",
                tentacle_specs.MCU_RPI_PICO_W,
            ),  # Tentacle v0.4
        ],
    )
    .add_testbed_instance(
        testbed_instance="ch_hans_2",
        tentacles=[
            ("e46340474b4c-2731", "v1.1", tentacle_specs.MCU_RPI_PICO2),
            ("e46340474b28-3623", "v1.0", tentacle_specs.DAQ_SALEAE),
            ("e46340474b0c-3523", "v1.0", tentacle_specs.DEVICE_POTPOURRY),
        ],
    )
    .add_testbed_instance(
        testbed_instance="ch_greenliff_1",
        tentacles=[
            ("e46340474b55-1722", "v1.0", tentacle_specs.MCU_RPI_PICO),
            ("e46340474b16-4d29", "v1.0", tentacle_specs.DAQ_SALEAE),
            ("e46340474b57-4722", "v1.0", tentacle_specs.DEVICE_POTPOURRY),
        ],
    )
    .add_testbed_instance(
        testbed_instance="au_damien_1",
        tentacles=[
            ("e46340474b14-1c29", "v1.1", tentacle_specs.MCU_RPI_PICO2),
            ("e46340474b12-1931", "v1.0", tentacle_specs.DAQ_SALEAE),
            ("e46340474b56-3b21", "v1.0", tentacle_specs.DEVICE_POTPOURRY),
        ],
    )
).inventory
