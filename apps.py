#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json,requests
from flask import Flask,redirect
from pathlib import Path
from feedly_notify import Feedly_notify

fn = Feedly_notify()

app = Flask(__name__)
@app.route("/<md5>")
def form(md5):
  p = Path(fn.cachedir) / Path(md5+".json")
  try:
    with p.open("r") as f:
      j = json.loads(f.read())
    result =  redirect(j["url"])
    postdata = {
      "type": "entries",
      "entryIds": [
        j["id"]
      ],
      "action": "markAsRead"
    }
  except:
    result = "Not found"
  r = requests.post("https://cloud.feedly.com/v3/markers",headers=fn.headers,json=postdata)
  return result
if __name__ == "__main__":
  app.run(port=49956)