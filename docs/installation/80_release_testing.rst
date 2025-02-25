Release testing
===================

For every release, the following tests will cover the main use cases.

Testgroup octoprobe
---------------------

.. code::

  op install

With 0, 1, and 2 tentacles connected.

.. code::

  op query
  op commissioning
  op powercycle infra --serial xy


Testgroup pytest
-------------------------

With 0, 1, and 2 tentacles connected.

.. code::


   # no flash - test installed firmware
   pytest

   # download firmware and flash
   # ATTENTION: The right mcu-tentacle has to be connected!
   pytest --firmware=pytest_args_firmware_RPI_PICO_v1.23.0.json
   pytest --firmware=pytest_args_firmware_RPI_PICO2_v1.24.0.json

   # clone firmware repo, compile in docker and flash
   pytest --firmware=https://github.com/micropython/micropython.git@v1.24.1


Testgroup Jupyter
-------------------------
