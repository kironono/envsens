# coding: utf-8

import asyncio

from .bme280 import BME280

class Worker(object):

    def __init__(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.device = BME280(0x76, 1)

    def run(self):
        self.task = self.loop.create_task(self.periodic_task())
        try:
            self.loop.run_until_complete(self.task)
        except KeyboardInterrupt as e:
            self.stop()

    async def periodic_task(self):
        while True:
            self.collect_data()
            await asyncio.sleep(3)

    def stop(self):
        self.task.cancel()

    def collect_data(self):
        self.device.readData()
