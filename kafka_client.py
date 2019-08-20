import os
import time
from we.eventcollector.ec import *

script_dir = os.path.dirname(__file__)
URL = "https://ec.luoxinshe.cn"

import time
import we.eventcollector.ec as event_collector
from we.eventcollector.serialization import parse_schema
import asyncio
import time
import os
script_dir = os.path.dirname(__file__)
URL = "https://ec.luoxinshe.cn"
class Kafka_Client:
    def __init__(self, appname,  version="v1", secret="a test secret", timeout=10):
        self.ec = event_collector.EventCollector(URL, appname, version, secret, timeout=timeout)
        #self.ec = event_collector.EventCollector(URL,"science", "v1", "recognize-test", timeout=5*60)
        print ('schema file: %s', os.path.join(script_dir,"./schema/activity_chn.avro"))
      

    def _set_loop(self):
        try:
            loop=asyncio.get_event_loop()
            print ('use event loop in main thread')
        except RuntimeError:
            print ('use event loop in spawned thread')
            loop=asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    async def _register_schema(self, filename, eventname):
        self.sender =  await self.ec.register_schema_from_file(filename, eventname)
    async def _send_data(self, json_data):
        print ('send async data')
        return await self.sender.send_event(json_data)

    def register_schema(self, filename, eventname):
        print ('register schema loop')
        self._set_loop()
        asyncio.get_event_loop().run_until_complete(self._register_schema(filename, eventname))
    def send_data(self, json_data):
        print ('send data loop')
        self._set_loop()
        asyncio.get_event_loop().run_until_complete(self._send_data(json_data))