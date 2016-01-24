#Soumyargha Sinha
#https://www.quora.com/profile/Soumyargha-Sam-Sinha
from bs4 import BeautifulSoup
import os
import urllib2
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
direc = os.path.dirname(os.path.abspath(__file__))
cyna = direc +"/CyanideHappiness"
if not os.path.exists(cyna):
	os.makedirs(cyna)
comic_no = 39
not_found = []
error505 = []
while(comic_no>0):
	url = "http://explosm.net/comics/"+str(comic_no)
	try:
    		getdata = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		check_newest = urllib2.urlopen("http://explosm.net/comics/archive")
		result = check_newest.read()
		souped = BeautifulSoup(result)	
		links = souped.find("div", { "class" : "small-3 medium-3 large-3 columns" })
		for hrefs in links.find_all("a"):
			href = hrefs.get('href').split('/')
			if href[2] == str(comic_no - 1):
				print "Finished downloading all comics till date. Go to sleep \n"
				print "Error 505 on " + error505 + "\n"
				print "Not found " + not_found + "\n"
				flag = 1
				break
			else:	
				print "Comic "+str(comic_no)+" not found. \n"
				not_found.append(comic_no)
				comic_no += 1
    				flag = 2
				break
		if flag == 1:
			break
		if flag == 2:
			continue
	print "downloading "+str(comic_no)
	result = getdata.read()
	souped = BeautifulSoup(result)
	com_image = souped.find("img", {"id": "main-comic"})
	img_link = "http:" + com_image.get('src')
	source = img_link.split('/')
	author = souped.findAll("small", { "class" : "author-credit-name" })
	for i in author:
		comic_folder = i.text
	if source[3] == "comics" or source[2] == "comics" or source[4] == "comics":
		try:
    			getcomic = urllib2.urlopen(img_link)
		except urllib2.HTTPError, e:
			print "Comic "+str(comic_no)+" cannot be downloaded. 505."
			error505.append(comic_no)
			comic_no += 1
			continue
		readcomic = getcomic.read()	
		savecomic = source[-1]
		filepath = direc +"/CyanideHappiness/"+ comic_folder
		if not os.path.exists(filepath):
			os.makedirs(filepath)
		name = source[-1]
		finalpath = os.path.join(filepath,name)
		with open (finalpath,"wb") as comic:
			comic.write(readcomic)
	comic_no += 1
