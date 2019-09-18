#!/usr/bin/python2.7 by kuronosuFear
import io
import json
import requests
import os
import time

def getAwesome(uri):
	sess = requests.Session()
	req = requests.Request('GET', 'https://jojo-p3-channel-or-jp.s3.amazonaws.com/' + uri, 
                       headers={
					   'X-Unity-Version': '2017.4.22f1',
					   'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)',
                       'Host': 'jojo-p3-channel-or-jp.s3.amazonaws.com',
					   'Connection': 'Keep-Alive',
                       'Accept-Encoding': 'gzip'})
	preq = req.prepare()
	for retries in range(10):
		try:
			response = sess.send(preq, timeout=10)
			response.raise_for_status()
			break
		except requests.exceptions.HTTPError as errh:
			print ('Http Error:',errh)
			time.sleep(5)
			pass
		except requests.exceptions.ConnectionError as errc:
			print ('Error Connecting:',errc)
			time.sleep(5)
			pass
		except requests.exceptions.Timeout as errt:
			print ('Timeout Error:',errt)
			time.sleep(5)
			pass
		except requests.exceptions.RequestException as err:
			print ('Oops: Something Else',err)
			time.sleep(5)
			pass
	return response.content

with open('Timestamp.txt', 'rb') as fo:
	timestamp=fo.read()

jsonResponse = json.loads(getAwesome('AssetBundles/' + timestamp + '/Android/Android.json'))

numberOfAssets = len(jsonResponse['bundles'])

path = timestamp+'\\'
if not os.path.exists(os.path.dirname(path)):
	try:
		os.makedirs(os.path.dirname(path))
	except OSError as exc: # Guard against race condition
		if exc.errno != errno.EEXIST:
			raise

for x in range(numberOfAssets):
	print('Downloading: ' + jsonResponse['bundles'][x]['name'])
	data=getAwesome('AssetBundles/' + timestamp + '/Android/'+ jsonResponse['bundles'][x]['name'])
	with open(path + jsonResponse['bundles'][x]['name'], 'wb') as fo:
		fo.write(data)
	dataManifest=getAwesome('AssetBundles/' + timestamp + '/Android/'+ jsonResponse['bundles'][x]['name'] + '.manifest')
	with open(path + jsonResponse['bundles'][x]['name']+'.manifest', 'wb') as fo:
		fo.write(dataManifest)
		
print('Download has finished!')