## DG Open Data

| Parameter | Status |
| ----------| ------ |
| Spatial | :heavy_check_mark: |
| Temporal | :heavy_check_mark: |
| Properties | :heavy_check_mark: |
| **kwargs | [limit] |

##### Properties
| Property | Type | Example |
|--------------------------|-------|-------------|
| eo:epsg | int | 4326 |
| legacy:event_name | str | 'california-wildfires' |
| legacy:timeframe | str | 'post-event' |

##### Notes
- There is no source API for this datasource, instead an index is created with the [dg-open-data-scraper](https://github.com/geospatial-jeff/dg-open-data-scraper).