# Настройки
threads_count = 10
user_agents   = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
proxies       = {
 #"http" : '149.56.106.104:3128',
 #"https": '149.56.106.104:3128',
}

import os
from requests import get
from random import choice
from threading import Thread
from bs4 import BeautifulSoup
from strgen import StringGenerator
os.system("clear")

print('''
          Автоматическое скачивание фотографий с prnt.sc
          ==============================================
               github.com/KaliSecurityMaxCreated 
''')


if not os.path.exists('img'):
	os.mkdir('img')

def save(url):
	file = url.split('/')[-1]
	try:
		data = get(url, allow_redirects = True, headers = user_agents, proxies = proxies)
	except:
		pass
	else:
		path = 'img/' + file
		open(path, 'wb').write(data.content)
		if os.path.exists(path):
			print('[+] Фото ' + file + ' Сохранено. Размер: ' + str(os.path.getsize(path)) + ' байт')

def scan():
	while True:

		random = StringGenerator('[\h]{6}').render().lower()
		url    = 'https://prnt.sc/' + random
		content = get(url, timeout = 3, headers = user_agents, proxies = proxies).text
		soup  = BeautifulSoup(content, 'html.parser')
		if 'Cloudflare' in soup.title.get_text().split():
			print('[-] Cloudflare заблокировал запрос!')
			break
		else:
			try:
				image = soup.img['src']
			except TypeError:
				continue
			else:
				if image.startswith('http'):
					save(image)


for i in range(1, threads_count):
	thread = Thread(target = scan)
	thread.start()
	print('[★] Ожидайте: ' + '[' + str(i) + '/' + str(threads_count) + ']')
