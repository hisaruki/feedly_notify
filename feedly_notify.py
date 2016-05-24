#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests,json,subprocess,hashlib,mimetypes,re
from pathlib import Path

class Feedly_notify:
  def markers(self):
    r = requests.get("https://cloud.feedly.com/v3/markers/counts",headers=self.headers)
    markers = json.loads(r.text)
    for marker in filter(lambda x:x["count"] > 0,markers["unreadcounts"]):
      yield marker

  def check(self):
    r = requests.get("https://cloud.feedly.com/v3/streams/contents?streamId="+self.streamid,headers=self.headers)
    contents = json.loads(r.text)
    try:
      items = contents["items"]
      items = filter(lambda x:x["unread"],items)
    except:
      items = []
    for item in items:
      try:
        visual = item["visual"]["url"]
      except:
        visual = None
      try:
        url = item["alternate"][0]["href"]
      except:
        url = item["originId"]
      yield item["title"],url,visual,item["id"]
      
  def notify(self,title,url,icon):
    notify = ["notify-send",'"'+title+'"',url]
    if icon:
      notify.append("-i")
      notify.append(icon)
    subprocess.Popen(notify)

  def __init__(self):
    conf = Path().home() / Path(".config/feedly_notify/config.json")
    try:
      with conf.open("r") as f:
        j = json.loads(f.read())
        token,streamid,cachedir = j["token"],j["streamid"],j["cachedir"]
    except:
      cachedir = str(Path().home() / Path(".cache/feedly_notify"))
      print("""Please visit:
    https://feedly.com/v3/auth/dev
    And paste the access token here.""")
      token = input('access token: ')
      print("")

    self.headers = {
      'content-type': 'application/json',
      'Authorization': 'OAuth ' + token
    }
    try:
      streamid
    except:
      streams = [x["id"] for x in markers()]
      streamid = list(filter(lambda x:re.match(r"^.*global.all$",x),streams))[0]
    if token and streamid:
      if not conf.parent.exists():
        conf.parent.mkdir(parents=True)
      with conf.open("w") as f:
        f.write(json.dumps({
          "token":token,
          "streamid":streamid,
          "cachedir":cachedir
        }))
    if not Path(cachedir).exists():
      Path(cachedir).mkdir(parents=True)

    self.streamid = streamid
    self.cachedir = cachedir
  def crawl(self):
    for title,url,visual,id in self.check():
      md5 = hashlib.md5(url.encode("utf-8")).hexdigest()
      p = Path(self.cachedir) / Path(md5+".json")
      if not p.exists():
        with p.open("w") as f:
          f.write(json.dumps({
            "url":url,
            "id":id
          }))
        try:
          r = requests.get(visual)
          ext = mimetypes.guess_extension(r.headers["Content-Type"])
          icon = Path(self.cachedir) / Path(md5+ext)
          with icon.open("wb") as f:
            f.write(r.content)
          icon = str(icon.resolve())
        except:
          icon = None
        yield title,"http://localhost:49956/"+md5,icon

