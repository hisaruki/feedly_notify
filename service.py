#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess,time,datetime
now = datetime.datetime.now()
last = datetime.datetime.now() - datetime.timedelta(minutes=15)
subprocess.Popen(["python3","apps.py"])
while 1 == 1:
  now = datetime.datetime.now()
  if (now-last).seconds > 90 * 10:
    subprocess.Popen(["python3","crawl.py"]).communicate()
    last = now
  time.sleep(1)
