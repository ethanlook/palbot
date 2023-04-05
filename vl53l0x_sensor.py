"""
Python implementation of the VL53L0X Time of Flight sensor for Viam.
"""

import asyncio
import logging
import sys
from typing import Any, Mapping

import adafruit_vl53l0x
import board
import busio
from viam.components.sensor import Sensor
from viam.rpc.server import Server


class VL53L0X(Sensor):
    def __init__(self, name: str):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        super().__init__(name)

    async def get_readings(self, **kwargs) -> Mapping[str, Any]:
        return {"range": self.vl53.range}


async def run(host: str, port: int, log_level: int):
    server = Server(
        components=[
            VL53L0X("vl53l0x"),
        ]
    )
    await server.serve(host=host, port=port, log_level=log_level)

if __name__ == "__main__":
    host = "localhost"
    port = 8081
    log_level = logging.DEBUG
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        level = sys.argv[3]
        if level.lower() == "q" or level.lower() == "quiet":
            log_level = logging.FATAL
    except (IndexError, ValueError):
        pass
    asyncio.run(run(host, port, log_level))
