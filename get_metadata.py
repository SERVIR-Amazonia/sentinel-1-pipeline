# connect to the API

import logging
logging.basicConfig(filename='access.log', level=logging.WARNING)

import psycopg2

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime, timedelta


def connect_to_db(db):
    try:
        connection_parameters = 'dbname=%s user=%s host=%s password=%s' % (db['dbname'], db['user'], db['host'], db['password'])
        conn = psycopg2.connect(connection_parameters)
    except Exception as e:
        print('problem connecting to the database!')
        logging.error(e)
    else:
        return conn, conn.cursor()

def close_connection(cur, conn):
    cur.close()
    conn.close()

db = {
    'dbname': 'DATABASE',
    'user': 'USERNAME',
    'host': 'localhost',
    'password': 'PASSWORD'
}

if __name__ == '__main__':
    start_year = 2019
    _date = datetime(start_year, 1, 1)
    condition = True
    while condition:
        try:
            api = SentinelAPI('USERNAME', 'PASSWORD', 'https://scihub.copernicus.eu/dhus')
            footprint = geojson_to_wkt(read_geojson('goldmine_sa.geojson'))
            products = api.query(
                footprint,
                date=(_date.strftime('%Y%m%d'), (_date+timedelta(days=1)).strftime('%Y%m%d')),
                platformname='Sentinel-1',
                producttype='GRD'
            )
        except Exception as e:
            print('{} for date: {}'.format(e, _date.strftime('%Y-%m-%d')))
            logging.error('{} for date: {}'.format(e, _date.strftime('%Y-%m-%d')))
        else:
            fc = api.to_geojson(products)
            features = fc['features']
            if len(features):
                print(_date)
                for feature in features:
                    properties = feature.properties
                    # properties
                    id = properties['id']
                    identifier = properties['identifier']
                    title = properties['title']
                    footprint = str(feature['geometry'])
                    #slave
                    acquisitiontype = properties['acquisitiontype']
                    beginposition = properties['beginposition']
                    endposition = properties['endposition']
                    filename = properties['filename']
                    format = properties['format']
                    #ingestiondate = properties.ingestiondate
                    instrumentname = properties['instrumentname']
                    instrumentshortname = properties['instrumentshortname']
                    lastorbitnumber = properties['lastorbitnumber']
                    lastrelativeorbitnumber = properties['lastrelativeorbitnumber']
                    quicklookiconname = properties['id']
                    #quicklookicondownloaded
                    missiondatatakeid = properties['missiondatatakeid']
                    orbitdirection = properties['orbitdirection']
                    orbitnumber = properties['orbitnumber']
                    platformidentifier = properties['platformidentifier']
                    polarisationmode = properties['polarisationmode']
                    productclass = properties['productclass']
                    producttype = properties['producttype']
                    relativeorbitnumber = properties['relativeorbitnumber']
                    sensoroperationalmode = properties['sensoroperationalmode']
                    size = properties['size']
                    slicenumber = properties['slicenumber']
                    swathidentifier = properties['swathidentifier']
                    #downloaded
                    #uploadedtogs
                    #uploadedtogee

                    conn, cur = connect_to_db(db)
                    cur.execute("INSERT INTO sentinel1 (id, identifier, title, footprint, acquisitiontype, beginposition, endposition, filename, format, instrumentname, instrumentshortname, lastorbitnumber, lastrelativeorbitnumber, quicklookiconname, missiondatatakeid, orbitdirection, orbitnumber, platformidentifier, polarisationmode, productclass, producttype, relativeorbitnumber, sensoroperationalmode, size, slicenumber, swathidentifier) VALUES ('{}', '{}', '{}', ST_GeomFromGeoJSON('{}'), '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(id, identifier, title, footprint, acquisitiontype, beginposition, endposition, filename, format, instrumentname, instrumentshortname, lastorbitnumber, lastrelativeorbitnumber, quicklookiconname, missiondatatakeid, orbitdirection, orbitnumber, platformidentifier, polarisationmode, productclass, producttype, relativeorbitnumber, sensoroperationalmode, size, slicenumber, swathidentifier))
                    conn.commit()
                    close_connection(conn, cur)

        _date += timedelta(days=1)
        if _date.year != start_year:
            condition = False
