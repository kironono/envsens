# coding: utf-8

import asyncio

from datetime import datetime, timedelta, timezone
from influxdb import InfluxDBClient
from .bme280 import BME280

class Worker(object):

    def __init__(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.device = BME280(0x76, 1)
        self.db = InfluxDBClient("localhost", 8086, None, None, "envsens")
        self.interval = 60

    def run(self):
        self.task = self.loop.create_task(self.periodic_task())
        try:
            self.loop.run_until_complete(self.task)
        except KeyboardInterrupt as e:
            self.stop()

    async def periodic_task(self):
        while True:
            self.collect_data()
            await asyncio.sleep(self.interval)

    def stop(self):
        self.task.cancel()

    def collect_data(self):
        timestr = datetime.now(timezone(timedelta(hours=+0), 'GMT')).strftime('%Y-%m-%dT%H:%M:%SZ')
        temperature, pressure, humidity = self.device.readData()
        point = {
            "measurement": "Environment",
            "tags": {
                "node": "node1",
            },
            "time": timestr,
            "fields": {
                "temperature": temperature,
                "pressure": pressure,
                "humidity": humidity,
            }

        }
        # print(point)
        self.db.write_points([point])
