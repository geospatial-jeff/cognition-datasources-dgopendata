import os
from datetime import datetime

from datasources.stac.query import STACQuery
from datasources.stac.item import STACItem
from datasources.sources.base import Datasource



class DGOpenData(Datasource):

    stac_compliant = False
    tags = ['EO', 'Satellite', 'Raster']

    def __init__(self, manifest):
        super().__init__(manifest)

    def search(self, spatial, temporal=None, properties=None, limit=10, **kwargs):
        from db import Database

        stac_query = STACQuery(spatial, temporal, properties)
        # candidates = stac_query.check_spatial(self.__class__.__name__)[:limit]
        with Database.load(read_only=True, deployed=True) as db:
            candidates = db.spatial_query({"type": "Feature", "geometry": stac_query.spatial})

        searches = 0
        for item in candidates:
            splits = item['link'].split('/')
            date = splits[-3]
            dt = datetime.strptime(date, '%Y-%m-%d')

            # Bbox
            xvals = [x[0] for x in item['geometry']['coordinates'][0]]
            yvals = [y[1] for y in item['geometry']['coordinates'][0]]
            bbox = [min(xvals), min(yvals), max(xvals), max(yvals)]

            if temporal:
                if not stac_query.check_temporal(dt):
                    continue

            timeframe = splits[-4]
            event_name = splits[-5]
            uid = splits[-2] + '_' + os.path.splitext(splits[-1])[0]

            item.update({'date': date, 'timeframe': timeframe, 'event_name': event_name, 'id': uid, 'bbox': bbox})

            if properties:
                item.update({'properties': stac_query})

            if searches < limit:
                self.manifest.searches.append([self, item])
                searches +=1

    def execute(self, query):
        stac_item = {
            'id': query['id'],
            'type': 'Feature',
            'bbox': query['bbox'],
            'geometry': query['geometry'],
            'properties': {
                'datetime': "{}T00:00:00.00Z".format(query['date']),
                'eo:epsg': int(query['eo:epsg']),
                'legacy:event_name': query['event_name'],
                'legacy:timeframe': query['timeframe']
            },
            'assets': {
                'data': {
                    'href': query['link'],
                    'title': 'Raster data'
                }
            }
        }

        # Validate item
        STACItem.load(stac_item)

        if "properties" in list(query):
            if query['properties'].check_properties(stac_item['properties']):
                return [stac_item]
        else:
            return [stac_item]