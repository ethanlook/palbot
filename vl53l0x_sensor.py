"""
Python implementation of the VL53L0X Time of Flight sensor for Viam.
"""

import asyncio
import logging
import os
import sys
import tempfile
from typing import Any, Optional, Tuple, Union

from PIL.Image import Image

import adafruit_vl53l0x
import board
import busio
import numpy as np
import open3d as o3d
from viam.components.camera import Camera
from viam.media.video import RawImage
from viam.rpc.server import Server


class VL53L0X(Camera):
    def __init__(self, name: str):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        super().__init__(name)

    async def get_point_cloud(self, *, timeout: Optional[float] = None, **kwargs) -> Tuple[bytes, str]:
        pc = o3d.geometry.PointCloud()
        points = np.array([[self.vl53.range / 1000, 0, 0]])
        pc.points = o3d.utility.Vector3dVector(points)
        path = os.path.join(tempfile.mkdtemp(), 'temp.pcd')
        o3d.io.write_point_cloud(path, pc)
        data = open(path, 'rb').read()
        return (data, "pointcloud/pcd")

    async def get_image(self, mime_type: str = "", *, timeout: Optional[float] = None, **kwargs) -> Union[Image, RawImage]:
        return await super().get_image(mime_type, timeout=timeout, **kwargs)

    async def get_properties(self, *, timeout: Optional[float] = None, **kwargs) -> Camera.Properties:
        return await super().get_properties(timeout=timeout, **kwargs)


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
    log_level = logging.ERROR
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        level = sys.argv[3]
        if level.lower() == "q" or level.lower() == "quiet":
            log_level = logging.FATAL
    except (IndexError, ValueError):
        pass
    asyncio.run(run(host, port, log_level))
