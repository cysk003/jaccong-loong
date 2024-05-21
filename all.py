import requests
import re
try:
  x = requests.get('https://fanmingming.com/txt?url=https://raw.githubusercontent.com/jaccong/loong/main/x.m3u',timeout=5).text
except Exception as e:
    print(f'x-error:【{e}】')
  
try:
  fmm = requests.get('https://fanmingming.com/txt?url=https://live.fanmingming.com/tv/m3u/ipv6.m3u',timeout=5).text
  fmm = re.sub(r'上海频道.*','',fmm,flags=re.DOTALL)
  fmm = re.sub('央视频道','[IPV6]央视频道',fmm)
  fmm = re.sub('卫视频道','[IPV6]卫视频道',fmm)
  fmm  =re.sub('数字频道','[IPV6]数字频道',fmm)
except Exception as e:
    print(f'fmm-error:【{e}】')
  
with open('litv.txt', 'r', encoding='utf-8') as file:
  litv = file.read()
with open('hk.txt', 'r', encoding='utf-8') as file:
  hk = file.read()
with open("all.txt", 'w', encoding='utf-8') as file:
  file.write(f'{x}\n')
  file.write(f'{fmm}\n')
  file.write(f'{litv}\n')
  file.write(f'{hk}\n')
