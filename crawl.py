#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from feedly_notify import Feedly_notify
fn = Feedly_notify()
for title,url,icon in fn.crawl():
  fn.notify(title,url,icon)