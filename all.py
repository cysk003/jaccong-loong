import requests

try:
  x = requests.get('https://raw.githubusercontent.com/jaccong/loong/main/x.m3u',timeout=1).text
except Exception as e:
    print(f'error:【{e}】')

with open('lity.txt', 'r', encoding='utf-8') as file:
  lity = file.read()

with open("all.txt", 'w', encoding='utf-8') as file:
  file.write(f'{x}\n')
  file.write(f'{lity}\n')
