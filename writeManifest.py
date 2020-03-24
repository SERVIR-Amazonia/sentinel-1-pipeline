# import library
import os
import logging
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime, timedelta
import json,ast


class functions(object):
	
	
	def __init__(self):
		pass
		
	def getDate(self,f):
		'split the filename to get the data'
		date = f.split("_")[4]
		year = int(date[0:4])
		month = int(date[4:6])
		day = int(date[6:8])
		return year, month, day
    
    
	def getUnixTime(self,f):
		'split the filename to get the data and return unix time'
		d = f.split("_")[4][0:8]
		t = datetime.strptime(d,'%Y%m%d') 
		t = (t- datetime(1970, 1, 1)).total_seconds()
		print int(t)
		return int(t)

	def getMetaData(self,year,month,day):
		
		try:
			_date = datetime(int(year), int(month), int(day))
			api = SentinelAPI('USERNAME', 'PASSWORD', 'https://scihub.copernicus.eu/dhus')
			footprint = geojson_to_wkt(read_geojson('goldmine_sa.geojson'))
			products = api.query(footprint,
							 date=(_date.strftime('%Y%m%d'), (_date+timedelta(days=1)).strftime('%Y%m%d')),
							 platformname='Sentinel-1',
							 producttype='GRD')
        
			fc = api.to_geojson(products)
			features =  fc['features']
			for items in features:
				if json.dumps(items['properties']['filename']).replace('"', '') == fn:
					metaData = items
			return metaData
		except:
			print 'couldnt retreive metadata'
			exit()


if __name__ == '__main__':
	
	function = functions()
	
	fileDir=os.listdir('/home/johnjdilger/sentinel1/output')
	
	
	for f in fileDir:
		fPar = f.partition("_Gamma0")
		fn =  fPar[0]+".SAFE"
		fjson = fPar[0]
		print fn
		fextension = fPar[1]+fPar[2]
		fextension = fextension.partition('mst_')[2]
	
		projectDir = "projects/earthengine-legacy/assets/projects/ACCA-SERVIR/Goldmining/SNAP/"
		bucketName = "gs://goldminehack/Sentinel1Output/"
		
		
		# set name	
		manifest = {}
		manifest['name'] = projectDir + fjson
		manifest['tilesets'] = [{"id": "VH_tileset", "crs": "EPSG:4326", "sources": [  {"uris": [ bucketName + fjson + "_Gamma0_VH_mst_"+fextension ] } ] },{"id": "VV_tileset", "crs": "EPSG:4326", "sources":  [ {"uris": [ bucketName + fjson + "_Gamma0_VV_mst_"+fextension] } ] }]					      
		manifest['bands'] = [{"id": "VV", "tileset_id": "VH_tileset"},{"id": "VH", "tileset_id": "VV_tileset"}]
		unixTime = function.getUnixTime(f)
		manifest['start_time'] = {"seconds": unixTime}
		year, month, day = function.getDate(f)
		metaData = function.getMetaData(year,month,day)	
		metaData = metaData['properties']	
		manifest['properties'] = ast.literal_eval(json.dumps(metaData))
		
		outname = '/home/johnjdilger/sentinel1/manifests/' + fjson + '.json'
		print manifest
		
		with open(outname, 'w') as fn:
			json.dump(manifest, fn, ensure_ascii=False, indent=4)



