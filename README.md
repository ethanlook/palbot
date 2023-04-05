# PalBot

PalBot is a rover built on the Viam platform.

## Setup

### Parts

Part | Qty | Cost
---- | --- | ----
Raspberry Pi 4 | 1 | ~$100
[VL53L0X](https://www.adafruit.com/product/3317) | 2 | $30

### Raspberry Pi 4

Follow Viam's [Raspberry Pi Setup Guide](https://docs.viam.com/installation/prepare/rpi-setup/). Be sure to [enable I2C](https://docs.viam.com/installation/#install-viam-server) for using the time of flight sensor.

[Install the `viam-server`](https://docs.viam.com/installation/#install-viam-server). [Install the Viam Python SDK](https://python.viam.dev/#installation) (use `pip3`).

[Install CircuitPython](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi) for using the time of flight sensor.

### VL53L0X Time of Flight Sensor

Wire up the VL53L0X to the Raspberry Pi during setup for verification.

![VL53L0X to Raspberry Pi](https://raw.githubusercontent.com/ethanlook/palbot/main/images/vl53l0x_verification_diagram.png)

Grab the script to use the sensor on the Viam robot. The process will be managed by the `viam-server` and will expose a gRPC service for getting sensor values.

```
curl -O https://raw.githubusercontent.com/ethanlook/palbot/main/vl53l0x_sensor.py
```

Add a new process in the Viam app under `CONFIG > PROCESSES`:

- Executable: `sudo`
- Argumentss: `-u`, `<user name>`, `python3`, `vl53l0x_sensor.py`
- Working directory: `/home/<user name>`

Add the sensor server as a remote in the Viam app under `CONFIG > REMOTES`:

```
{
  "prefix": true,
  "address": "localhost:8081",
  "name": "vl53l0x"
}
```

Verify the sensor is working in the Viam app under `CONTROL > Sensors`.

![VL53L0X sensor readings](https://raw.githubusercontent.com/ethanlook/palbot/main/images/vl53l0x_sensor_readings.gif)