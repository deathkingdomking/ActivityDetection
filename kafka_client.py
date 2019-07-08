import time

from we.eventcollector.ec import *
from we.eventcollector.serialization import parse_schema
from schema.actvity import *
import asyncio
import time
import os

script_dir = os.path.dirname(__file__)
URL = "https://ec.luoxinshe.cn"

class Kafka_Client:

	def __init__(self):	
		self.ec = EventCollector(URL,"science", "v1", "recognize-test", timeout=5*60)
		reg = lambda: ec.register_schema_from_file(os.path.join(script_dir,"./schema/activity_chn.avsc"), "test")
		asyncio.get_event_loop().run_until_complete(reg())
		event = activity_data
		async def reg_and_send():
	 		sender = await reg()
	 		await sender.send_event(event)
	 		await sender.send_event(event, sender.version)
		asyncio.get_event_loop().run_until_complete(reg_and_send())

