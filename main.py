from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
from datetime import datetime
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ['APP_ID']
app_secret = os.environ['APP_SECRET']

user_id = os.environ['USER_ID']
template_id = os.environ['TEMPLATE_ID']

week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]


def get_weather():
  url = "https://v0.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid=&city=" + city
  res = requests.get(url).json()
  weather = res['data'][0]
  return weather['wea'], math.floor(int(weather['tem'])), math.floor(int(weather['tem1'])), math.floor(int(weather['tem2']))


def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_wed_count():
  delta = today - datetime.strptime('2021-06-01', "%Y-%m-%d")
  return delta.days


def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,lowest,highest = get_weather()

data = {"date":{"value":week_list[datetime.today().weekday()]}"weather":{"value":wea},"temperature":{"value":temperature},"lowest":{"value":lowest},"highest":{"value":highest},"love_days":{"value":get_count()},"wed_days":{"value":get_wed_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
