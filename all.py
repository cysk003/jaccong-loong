import requests

try:
  x = requests.get('https://fanmingming.com/txt?url=https://raw.githubusercontent.com/jaccong/loong/main/x.m3u',timeout=5).text
except Exception as e:
    print(f'error:【{e}】')

with open('litv.txt', 'r', encoding='utf-8') as file:
  litv = file.read()

with open("all.txt", 'w', encoding='utf-8') as file:
  file.write(f'{x}\n')
  file.write(f'{litv}\n')
