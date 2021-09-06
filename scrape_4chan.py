#!/usr/bin/env python3
'''
	4chan/4channel file scraper
	
	Requires:
		BeautifulSoup4
		wget, youtube-dl
	
	Scrapes:
		User-posted files.
	
	Usage:
		$ python3 scrape_reddit.py https://boards.4channel.org/wsg/thread/00000000
		$ python3 scrape_reddit.py https://boards.4chan.org/r/thread/00000000
	
	Extra Configuration:
		bool: SAVE_AS_TITLE_INSTEAD_OF_POST_ID
	
	License:
		Attribution-ShareAlike 4.0 International
		https://creativecommons.org/licenses/by-sa/4.0/
		Julian Cahill <cahill.julian@gmail.com>
'''
from bs4 import BeautifulSoup
import sys, os, requests, re, subprocess

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

SAVE_AS_TITLE_INSTEAD_OF_POST_ID = False

default_wget_command = lambda folder: ['wget', '-nv', '-U', headers['User-Agent'], '-P', folder]

def scrape(folder, data):
	soup = BeautifulSoup(data, 'lxml')
	
	for obj in soup.select('.file .fileText'):
		anchor = obj.select('a')[0]
		
		if not anchor or not (anchor.get('href') and anchor.get('title')):
			continue
		
		href = anchor.get('href')
		title = anchor.get('title')
		
		if href.startswith('//'):
			href = 'https:' + href
		
		if re.match('^https?://', href):
			if SAVE_AS_TITLE_INSTEAD_OF_POST_ID:
				yield ['wget', '-nv', '-U', headers['User-Agent'], '-P', folder, href, '-O', f'{folder}/{title}']
			else:
				yield ['wget', '-nv', '-U', headers['User-Agent'], '-P', folder, href]
		else:
			yield ['echo', 'Got a funky URL:', href]
		

if __name__ == "__main__":
	url = sys.argv[1]
	req = requests.get(url, headers=headers)
	
	# determine the folder to write to
	expr = r'/thread/(\d+)/?$'
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
	
	# generate the commands
	commands = list(scrape(folder, req.content))
	
	print(f'I will run these ({len(commands)}) commands:')
	for command in commands:
		print('$', *command)
	
	if input('Continue?').startswith('n'):
		sys.exit(2)
	
	for command in commands:
		print('$', *command)
		subprocess.check_output(command)