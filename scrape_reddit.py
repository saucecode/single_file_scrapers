'''
	reddit.com listing scraper
	
	Requires:
		wget, youtube-dl
	
	Scrapes:
		i.imgur.com  images, mp4, and gifv
		i.redd.it    images
		v.redd.it    videos
		redgifs.com  videos
		gfycat.com   videos
		
		Media only. No comment threads, no text posts.
	
	Usage:
		Must specify a /.json reddit page link.
		
		$ python3 scrape_reddit.py https://reddit.com/r/aww/.json
	
	Usage Tips:
		Add these GET queries to achieve more results:
			?limit=100         -- gets 100 items
			?after=t3_xxxxxx   -- retrieves posts after the given
			                      post ID (for fetching the next page)
	
	License:
		Attribution-ShareAlike 4.0 International
		https://creativecommons.org/licenses/by-sa/4.0/
		Julian Cahill <cahill.julian@gmail.com>
'''

import json, requests, sys, re, subprocess, os

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

default_wget_command = lambda folder: ['wget', '-Nv', '-nv', '-U', headers['User-Agent'], '-P', folder]

scrape_definitions = {
	r'^https?://i\.redd\.it/.*$':
		lambda folder, url: [*default_wget_command(folder), url],
	
	r'^https?://v\.redd\.it/.*$':
		lambda folder, url: ['youtube-dl', '-o', f'{folder}/%(title)s-%(id)s.%(ext)s', '--user-agent', headers['User-Agent'], url],
		
	r'^https?://i\.imgur\.com/.*\..{3}$':
		lambda folder, url: [*default_wget_command(folder), url],
		
	r'^https?://i\.imgur\.com/.+\.gifv$':
		lambda folder, url: [*default_wget_command(folder), f'{url[:-4]}mp4'],
	
	r'^https?://redgifs.com/watch/.+$':
		lambda folder, url: ['youtube-dl', '-o', f'{folder}/%(title)s-%(id)s.%(ext)s', '--user-agent', headers['User-Agent'], url],
	
	r'^https?://gfycat.com/.+$':
		lambda folder, url: ['youtube-dl', '-o', f'{folder}/%(title)s-%(id)s.%(ext)s', '--user-agent', headers['User-Agent'], url]
}

def scrape(folder, data):
	for item in data['data']['children']:
		item_url = item['data'].get('url', '')
		
		found = False
		
		for expr, func in scrape_definitions.items():
			if re.fullmatch(expr, item_url):
				yield func(folder, item_url)
				found = True
				break
		
		if not found:
			yield ['echo', 'Unknown handler for "' + item_url + '"']

if __name__ == "__main__":
	url = sys.argv[1]
	req = requests.get(url, headers=headers)
	data = req.json()
	
	expr = r'/(\w+)/.json'
	if not (folder := re.findall(expr, url)):
		print('Could not determine a folder for url:', url)
		sys.exit(1)
	else:
		folder = folder[0]
	
	if not os.path.exists(folder):
		print('Creating new folder:', folder)
		os.mkdir(folder)
	else:
		if os.path.isdir(folder):
			print('Using existing folder:', folder)
		else:
			print('Unable to use folder:', folder)
	
	commands = list(scrape(folder, data))
	
	print(f'I will run these ({len(commands)}) commands:')
	for command in commands:
		print('$', *command)
	
	if input('Continue?').startswith('n'):
		sys.exit(2)
	
	for command in commands:
		print('$', *command)
		subprocess.check_output(command)