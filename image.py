#参考：https://qiita.com/Jixjia/items/881c03c50c6f07b0b6ab

import bs4
import requests
import re
import urllib.request, urllib.error
import os
import argparse
import sys
import json


def get_soup(url,header):
	return bs4.BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

def main(args, PenguinName):
	search = urllib.parse.quote(PenguinName)
	parser = argparse.ArgumentParser(description = 'Options for scraping Google images')
	parser.add_argument('-s', '--search', default = search, type = str, help = 'search term')
	args = parser.parse_args()

	query = args.search.split()
	query = '+'.join(query)
	max_images = 100

	save_directory = "PenguinImages" + '/' + query
	save_directory = urllib.parse.unquote(save_directory)	#URLのクエリをパース
	if not os.path.exists(save_directory):
		os.makedirs(save_directory)

	# スクレーピング
	url = "https://www.google.co.jp/search?q=" + query + "&source=lnms&tbm=isch"
	header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)
	ActualImages = []

	for a in soup.find_all("div", {"class":"rg_meta"}):
		link, Type = json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
		ActualImages.append((link,Type))
	for i, (img, Type) in enumerate(ActualImages[0:max_images]):
		try:
			Type = Type if len(Type) > 0 else 'jpg'
			print("Downloading image {} ({}), type is {}".format(i, img, Type))
			raw_img = urllib.request.urlopen(img).read()
			f = open(os.path.join(save_directory, "img_" + str(i) + "." + Type), 'wb')
			f.write(raw_img)
			f.close()
		except Exception as e:
			print ("could not load : " + img)
			print (e)

if __name__ == '__main__':
	from sys import argv
	try:
		PenguinList = ["エンペラーペンギン", "キングペンギン", "アデリーペンギン", "ヒゲペンギン", "ジェンツーペンギン", "ロイヤルペンギン", "マカロニペンギン", "スネアーズペンギン", "シュレーターペンギン", "イワトビペンギン", "フィヨルドランドペンギン", "ケープペンギン", "マゼランペンギン", "フンボルトペンギン", "ガラパゴスペンギン", "キガシラペンギン", "コガタペンギン", "ハネジロペンギン", "Emperor Penguin", "King Penguin", "Adelie Penguin", "Chinstrap Penguin", "Gentoo Penguin", "Royal Penguin", "Macaroni Penguin", "Snares penguin", "Erect-crested Penguin", "Rockhopper Penguin", "Fiordland Penguin", "African Penguin", "Magellanic Penguin", "Humboldt Penguin", "Galápagos Penguin", "Yellow-eyed Penguin", "Little Penguin", "White-flippered Penguin"]
		for Penguin in PenguinList:
			main(argv, Penguin)
	except KeyboardInterrupt:
		pass
	sys.exit()