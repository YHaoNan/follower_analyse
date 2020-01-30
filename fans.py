#!/usr/bin/env python
# coding=utf-8
import requests
import logging
import json
import time

sleep_time = 60*10
while True:
	LOG_FORMAT = "%(asctime)s-%(message)s"
	DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
	logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)
	resp = requests.get("https://m.weibo.cn/api/container/getIndex?containerid=1005051927305954")
	if resp.status_code != 200:
		logging.warning("Error, code is %d"%resp.status_code)
	else:
		try:
			jo = json.loads(resp.text)
			fcnt = jo["data"]["userInfo"]["followers_count"]
			logging.info(fcnt)
		except:
			logging.info("There is an exception raised!")
	time.sleep(sleep_time)
