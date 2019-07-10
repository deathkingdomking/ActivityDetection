import time

import we.eventcollector.ec as event_collector
from we.eventcollector.serialization import parse_schema
from schema import activity_chn
import asyncio
import time
import os

script_dir = os.path.dirname(__file__)
URL = "https://ec.luoxinshe.cn"


class Kafka_Client:

	def __init__(self):	
		self.ec = event_collector.EventCollector(URL,"science", "v1", "recognize-test", timeout=5*60)
		event = activity_chn.sample_activity_chn_data

		print ('schema file: %s', os.path.join(script_dir,"./schema/activity_chn.avro"))
		print ('event to push: %s', event)

		reg = lambda: event_collector.EventCollector.register_schema_from_file(os.path.join(script_dir,"./schema/activity_chn.avro"), "test")
		asyncio.get_event_loop().run_until_complete(reg())
		async def reg_and_send():
	 		sender = await reg()
	 		await sender.send_event(event)
	 		await sender.send_event(event, sender.version)
		asyncio.get_event_loop().run_until_complete(reg_and_send())

