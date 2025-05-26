Installation Ubuntu
===================

Target OS: Ubuntu Server 24.04.1 LTS.

To set up a Raspberry Pi 4/5, start with :doc:`20_raspberry`.

Installation: Users
-------------------

Octoprobe user: `octoprobe`
Github runner user: `githubrunner`

.. code::

    sudo adduser octoprobe
    sudo adduser githubrunner

Do not forget to config git:

.. code::

    git config --global user.name "Hans Maerki"
    git config --global user.email "buhtig.hans.maerki@ergoinfo.ch"


Installation: APT
-----------------

.. code::

    sudo apt update \
      && sudo apt upgrade -y \
      && sudo apt install -y git uhubctl dfu-util \
        python-is-python3 \
        docker.io docker-buildx

    sudo groupadd docker
    sudo usermod -aG docker,plugdev,dialout,systemd-journal octoprobe
    sudo usermod -aG docker,plugdev,dialout,systemd-journal githubrunner

    sudo snap install astral-uv --classic


git clone testbed_showcase
--------------------------

.. code::

    git clone https://github.com/octoprobe/testbed_showcase.git

python
------

.. code::

    cd ~/testbed_showcase

    uv venv --python 3.13.3

    source .venv/bin/activate
    uv pip install --upgrade -e .

    echo 'source ~/testbed_showcase/.venv/bin/activate' >> ~/.profile
    # Log out and in again

Software requiring elevated access
----------------------------------

Will be used by usbhubctl, mpremote and various firmware programmes


.. code::

    op install

Now `op install` will instruct you to:

.. code::

    echo 'PATH=$HOME/octoprobe_downloads/binaries/x86_64:$PATH' >> ~/.profile
    sudo cp /home/maerki/work_octoprobe_octoprobe/src/octoprobe/udev/*.rules /etc/udev/rules.d
    sudo sudo udevadm control --reload-rules
    sudo sudo udevadm trigger

These commands may help for debugging udev rules:

.. code::

  sudo udevadm control --log-priority=debug
  sudo journalctl -u systemd-udevd.service -f | grep 82-octoprobe

  sudo udevadm monitor -e
  sudo udevadm control --reload-rules
  sudo udevadm trigger --type=devices --action=change

Run your first tests
--------------------

Connect tentacles:

* 1 tentacle_DAQ_SALEAE
* 1 tentacle_DEVICE_PORTPOURRY
* 1-n tentacle_MCU_xx

Start the tests

.. code:: 

   cd ~/testbed_showcase
   pytest --firmware=pytest_args_firmware_RPI_PICO2_v1.24.0.json tests/test_simple.py::test_i2c
