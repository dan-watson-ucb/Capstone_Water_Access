# dc-addons

These [dc.js](http://dc-js.github.io/dc.js/) addons provide new charts for the dc namespace.

## Addons
  * [Leaflet.js](#leafletjs)
  * [Google Maps](#google-maps)
  * [Tooltip Mixin](#tooltip-mixin)
  * [Pagination Mixin](#pagination-mixin)
  * [Bubble Cloud](#bubble-cloud)
  * [Paired Row](#paired-row)
  * [Server](#server)
  * [AngularJS Directives](#angularjs-directives)
  * [Crossfilter Server](#crossfilter-server)
  * [Crossfilter Server With Elastic Search](#crossfilter-server-with-elastic-search)

## Installation
```js
bower install dc-addons --save
npm install dc-addons --save
```

You can either include all addons or each on individually as you need them.  To see examples of individual addons see each addon below. The following example will include all addons.
```html
<!-- dc-addons requirements -->
<link rel="stylesheet" href="bower_components/leaflet/dist/leaflet.css" />
<script src="bower_components/leaflet/dist/leaflet.js"></script>
<link rel="stylesheet" href="bower_components/leaflet.markercluster/dist/MarkerCluster.css" />
<link rel="stylesheet" href="bower_components/leaflet.markercluster/dist/MarkerCluster.Default.css" />
<script src="bower_components/leaflet.markercluster/dist/leaflet.markercluster.js"></script>
<script src="https://maps.googleapis.com/maps/api/js?key=API_KEY"></script>
<script src="http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclusterer/src/markerclusterer.js"></script>script>
<script src="bower_components/d3-tip/index.js"></script>

<!-- dc-addons -->
<link rel="stylesheet" href="bower_components/dc-addons/dist/dc-addons.min.css" />
<script src="bower_components/dc-addons/dist/dc-addons.min.js"></script>
```

## Leaflet.js

This extension provides support for dc.js charts in a [leaflet.js](http://leafletjs.com/) map. This is an extension of https://github.com/yurukov/dc.leaflet.js updated to work with dc.js version 2.

#### Usage
There are two charts currently implemented - markers and choropleth. They extend the base abstract leaflet chart. Both support selection of datapoints and update in real time. Styling and map options can be set directly to the map object and though functions in the chart. Check the [Leaflet reference](http://leafletjs.com/reference.html#map-options) for more information on the specific map, marker and geojson options.
Location can be set as either 'lat,lng' string or as an array [lat,lng].

###### Marker Chart
Each group is presented as one marker on the map.
```
dc.leafletMarkerChart(parent,chartGroup)
  .mapOptions({..})       - set leaflet specific options to the map object; Default: Leaflet default options
  .center([1.1,1.1])      - initial location
  .zoom(7)                - initial zoom level
  .map()                  - get map object
  .locationAccessor()     - function (d) to access the property indicating the latlng (string or array); Default: keyAccessor
  .marker()               - set function (d,map) to build the marker object. Default: standard Leaflet marker is built
  .icon()                 - function (d,map) to build an icon object. Default: L.Icon.Default
  .popup()                - function (d,marker) to return the string or DOM content of a popup
  .renderPopup(true)      - set if popups should be shown; Default: true
  .cluster(false)         - set if markers should be clustered. Requires leaflet.markercluster.js; Default: false
  .clusterObject({..})    - options for the markerCluster object
  .rebuildMarkers(false)  - set if all markers should be rebuild each time the map is redrawn. Degrades performance; Default: false
  .brushOn(true)          - if the map would select datapoints; Default: true
  .filterByArea(false)    - if the map should filter data based on the markers inside the zoomed in area instead of the user clicking on individual markers; Default: false
  .markerGroup()          - get the Leaflet group object containing all shown markers (regular group or cluster)
  .popupOnHover(false)    - whether or not to display the popup when hovering the marker instead of click; Default: false
  .title()                - The html title attribute of the markers
  .fitOnRender(true)      - Whether or not to automatically position the map to fit all markers on the display after the initial rendering; Default: true
  .fitOnRedraw(false)     - Whether or not to automatically position the map to fit all markers on the display after the markers have been cross filtered; Default: false
  .tiles()                - function (map) return a new L.tileLayer object to set a custom tile;
```

###### Choropleth Chart
Each group is mapped to an feature on the map
```
dc.leafletChoroplethChart(parent,chartGroup)
  .mapOptions({..})       - set leaflet specific options to the map object; Default: Leaflet default options
  .center([1.1,1.1])      - get or set initial location
  .zoom(7)                - get or set initial zoom level
  .map()                  - get map object
  .geojson()              - geojson object describing the features
  .featureOptions()       - object or a function (feature, v) to set the options for each feature - warning this will override the d3 color scheming
  .featureKeyAccessor()   - function (feature) to return a feature property that would be compared to the group key; Defauft: feature.properties.key
  .popup()                - function (d,feature) to return the string or DOM content of a popup
  .renderPopup(true)      - set if popups should be shown; Default: true
  .brushOn(true)          - if the map would select datapoints; Default: true
  .legend(dc.leafletLegend().position('bottomright'))
```

###### Custom Chart
Gives you full control over what is displayed on the map
```
dc.leafletCustomChart(parent,chartGroup)
  .mapOptions({..})       - set leaflet specific options to the map object; Default: Leaflet default options
  .center([1.1,1.1])      - initial location
  .zoom(7)                - initial zoom level
  .map()                  - get map object
  .locationAccessor()     - function (d) to access the property indicating the latlng (string or array); Default: keyAccessor
  .renderItem()           - function (chart, map, d, i) the initial rendering of the map
  .redrawItem()           - function (chart, map, d, i) run on every crossfilter. The d object will have a filtered value added to it.
```


#### Examples
  * [Leaflet Marker](http://intellipharm.github.io/dc-addons/examples/leaflet-marker.html)
  * [Leaflet Choropleth](http://intellipharm.github.io/dc-addons/examples/leaflet-choropleth.html)
  * [Leaflet Custom](http://intellipharm.github.io/dc-addons/examples/leaflet-custom.html)


#### Requirements

These are the requirements for the dc leaflet charts. Ther version number supplied is the version supported when created. It could work with later versions.

  *  [leaflet.js](https://github.com/Leaflet/Leaflet) v0.7.2
```html
<!--- through bower -->
<link rel="stylesheet" href="bower_components/leaflet/dist/leaflet.css" />
<script src="bower_components/leaflet/dist/leaflet.js"></script>

<!--- through cdn -->
<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css" />
<script src="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.js"></script>
```
  *  [leaflet.markercluster.js](https://github.com/Leaflet/Leaflet.markercluster) v0.4.0 (in case you use the cluster option)
```html
<!--- through bower -->
<link rel="stylesheet" href="bower_components/leaflet.markercluster/dist/MarkerCluster.css" />
<link rel="stylesheet" href="bower_components/leaflet.markercluster/dist/MarkerCluster.Default.css" />
<script src="bower_components/leaflet.markercluster/dist/leaflet.markercluster.js"></script>

<!--- through cdn -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster.js"></script>
```

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/leaflet-map/dc-leaflet.min.js"></script>
```

## Google Maps

This extension provides support for dc.js charts in a [google](https://developers.google.com/maps/documentation/javascript/) map. This is an extension of https://github.com/yurukov/dc.leaflet.js modified to work with google maps and dc.js version 2.

#### Usage
There are two charts currently implemented - markers and choropleth. They extend the base abstract google chart. Both support selection of datapoints and update in real time. Styling and map options can be set directly to the map object and though functions in the chart. Check the [Google maps reference](https://developers.google.com/maps/documentation/javascript/reference) for more information on the specific map, marker and geojson options.
Location can be set as either 'lat,lng' string or as an array [lat,lng].

###### Marker Chart
Each group is presented as one marker on the map.
```
dc.googleMarkerChart(parent,chartGroup)
  .mapOptions({..})       - set google maps specific options to the map object; Default: Google maps default options
  .center([1.1,1.1])      - initial location
  .zoom(7)                - initial zoom level
  .map()                  - get map object
  .locationAccessor()     - function (d) to access the property indicating the latlng (string or array); Default: keyAccessor
  .marker()               - set function (d,map) to build the marker object. Default: standard Google map marker is built
  .icon()                 - function (d,map) to build an icon object. Default: L.Icon.Default
  .popup()                - function (d,marker) to return the string or DOM content of a popup
  .renderPopup(true)      - set if popups should be shown; Default: true
  .cluster(false)         - set if markers should be clustered. Requires markerclusterer; Default: false
  .clusterObject({..})    - options for the markerCluster object
  .rebuildMarkers(false)  - set if all markers should be rebuild each time the map is redrawn. Degrades performance; Default: false
  .brushOn(true)          - if the map would select datapoints; Default: true
  .filterByArea(false)    - if the map should filter data based on the markers inside the zoomed in area instead of the user clicking on individual markers; Default: false
  .markerGroup()          - get the Google maps group object containing all shown markers (regular group or cluster)
  .title()                - The html title attribute of the markers
  .fitOnRender(true)      - Whether or not to automatically position the map to fit all markers on the display after the initial rendering; Default: true
  .fitOnRedraw(false)     - Whether or not to automatically position the map to fit all markers on the display after the markers have been cross filtered; Default: false
```

###### Choropleth Chart
Each group is mapped to an feature on the map
```
dc.googleChoroplethChart(parent,chartGroup)
  .mapOptions({..})       - set google maps specific options to the map object; Default: Google maps default options
  .center([1.1,1.1])      - get or set initial location
  .zoom(7)                - get or set initial zoom level
  .map()                  - get map object
  .geojson()              - geojson object describing the features
  .featureOptions()       - object or a function (feature) to set the options for each feature
  .featureKeyAccessor()   - function (feature) to return a feature property that would be compared to the group key; Defauft: feature.properties.key
  .popup()                - function (d,feature) to return the string or DOM content of a popup
  .renderPopup(true)      - set if popups should be shown; Default: true
  .brushOn(true)          - if the map would select datapoints; Default: true
```

###### Custom Chart
Gives you full control over what is displayed on the map
```
dc.googleCustomChart(parent,chartGroup)
  .mapOptions({..})       - set google specific options to the map object; Default: Google default options
  .center([1.1,1.1])      - initial location
  .zoom(7)                - initial zoom level
  .map()                  - get map object
  .locationAccessor()     - function (d) to access the property indicating the latlng (string or array); Default: keyAccessor
  .renderItem()           - function (chart, map, d, i) the initial rendering of the map
  .redrawItem()           - function (chart, map, d, i) run on every crossfilter. The d object will have a filtered value added to it.
```


#### Examples
  * [Google Marker](http://intellipharm.github.io/dc-addons/examples/google-marker.html)
  * [Google Choropleth](http://intellipharm.github.io/dc-addons/examples/google-choropleth.html)
  * [Google Custom](http://intellipharm.github.io/dc-addons/examples/google-custom.html)


#### Requirements
  * [google maps](https://developers.google.com/maps/documentation/javascript/)
```html
<!--- through cdn -->
<script src="https://maps.googleapis.com/maps/api/js?key=API_KEY"></script>
```
  * [google maps marker clusterer](https://code.google.com/p/google-maps-utility-library-v3/)
```html
<!--- through cdn -->
<script src="http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclusterer/src/markerclusterer.js"></script>script>
```

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/google-map/dc-google.min.js"></script>
```

## Tooltip Mixin
This allows you to add html and style the chart title

#### Usage
After you have rendered the chart than run the tooltip mixin on the chart

```js
var chart = dc.barChart('#chart');
// set options...
chart.render();

dc.tooltipMixin(chart);
```


#### Examples
Coming soon...


#### Requirements
  * [d3-tip](https://github.com/Caged/d3-tip)
```html
<!-- through bower -->
<script src="bower_components/d3-tip/index.js"></script>
<!-- through cdn -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3-tip/0.6.3/d3-tip.min.js"></script>
```

If you want to include individually
```html
<link type="stylesheet" href="bower_components/dc-addons/dist/tooltip/dc-tooltip-mixin.min.css" />
<script src="bower_components/dc-addons/dist/tooltip/dc-tooltip-mixin.min.js"></script>
```

## Pagination Mixin
This allows you to paginate a chart

#### Usage
After you have rendered the chart than run the pagination mixin on the chart

```js
var chart = dc.barChart('#chart');
// set options...
chart.render();

dc.paginationMixin(chart);
```


#### Examples
  * [Pagination](http://intellipharm.github.io/dc-addons/examples/pagination.html)


#### Requirements
None

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/pagination/dc-pagination-mixin.min.js"></script>
```

## Bubble Cloud

#### Usage
```js
var chart = dc.bubbleCloud('#chart');

// required options
chart
    .width(500)
    .height(500)
    .dimension(dimension)
    .group(group)
    .x(d3.scale.ordinal())
    .r(d3.scale.linear())
    .radiusValueAccessor(function(d) {
        return d.value;
    })

// optional options
chart
    valueAccessor(function(d) {
        return d.value;
    })
    .colorAccessor(function(d) {
        return d.value;
    })
    .label(function(d) {
        return d.key;
    })
    .renderLabel(true)
    .title(function(d) {
        return d.key + ': ' + d.value;
    })
    .renderTitle(true)

```

#### Examples
  * [Bubble Cloud](http://intellipharm.github.io/dc-addons/examples/bubble-cloud.html)


#### Requirements
None

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/bubble-cloud/dc-bubble-cloud.min.js"></script>
```


## Paired Row
Two row charts beside each other, usually used for gender/age breakdowns

#### Usage
```js
var chart = dc.pairedRowChart('#chart');

// the dimension is required to return an array
var ndx = crossfilter(experiments),
    ageGenderDimension = ndx.dimension(function(d) {
        var age_range = 'Unknown';

        if (d.age <= 9) {
            age_range = '0 - 9';
        } else if (d.age <= 19) {
            age_range = '10 - 19';
        } else if (d.age <= 29) {
            age_range = '20 - 29';
        } else if (d.age <= 39) {
            age_range = '30 - 39';
        } else if (d.age <= 49) {
            age_range = '40 - 49';
        } else if (d.age <= 59) {
            age_range = '50 - 59';
        } else if (d.age <= 69) {
            age_range = '60 - 69';
        } else if (d.age <= 79) {
            age_range = '70 - 79';
        } else if (d.age <= 89) {
            age_range = '80 - 89';
        } else if (d.age <= 99) {
            age_range = '90 - 99';
        } else if (d.age >= 100) {
            age_range = '100+';
        }

        return [d.gender, age_range];
    }),
    ageGenderGroup = ageGenderDimension.group().reduceCount();

// required options
chart
    .width(500)
    .height(500)
    .dimension(dimension)
    .group(group)
    // tells the left chart to filter the data based on this function
    .leftKeyFilter(function(d) {
        return d.key[0] === 'Male';
    })
    // tells the right chart to filter the data based on this function
    .rightKeyFilter(function(d) {
        return d.key[0] === 'Female';
    })

// optional options - this chart extends dc.rowChart, so it has all the same options.

```

#### Demo
  * [Paired Row Chart](http://intellipharm.github.io/dc-addons/examples/paired-row-chart.html)


#### Requirements
None

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/paired-row/dc-paired-row-chart.min.js"></script>
```

## Server
Charts generated on the server for large datasets. Only the following charts currently work:

  * Pie
  * Bar
  * Row
  * Line

#### Usage
```js
var chart = dc.serverChart('#chart');

chart
    .options({
        // required options
        server: 'http://127.0.0.1:3000/',
        name: 'my-chart', // The name of the object in the config file

        // optional options
        errorMessage: 'A problem occurred creating the charts. Please try again later',
        loadingMessage: 'Loading',
        reconnectingMessage: 'There appears to be a problem connecting to the server. Retyring...',
        connectionErrorMessage: 'Could not connect to the server.',
    })
    .render();
```

To get the server running

```
iojs index [full path to server-config.js]
```

The server-config.js file should look something like this.

```js
var dc = require('dc');

module.exports = {
    'my-chart': {
        connection:  {
            host: 'localhost',
            username: 'root',
            password: 'password',
            database: 'my-database',
            sql: 'SELECT * FROM members'
        },
        charts: [
            {
                type: 'pieChart',
                options: {
                    width: 250,
                    height: 250,
                    margins: {
                        top: 30,
                        right: 50,
                        bottom: 25,
                        left: 40
                    },
                    dimension: function (d) {
                        if (d.gender === 0) {
                            return 'Male';
                        } else if (d.gender === 1) {
                            return 'Female';
                        }

                        return 'Unknown';
                    },
                    group: function (dimension) {
                        return dimension.group().reduceCount();
                    }
                }
            }
        ]
    },
};
```

#### Demo
You will need to clone and run the server locally for an example


#### Requirements
  * [iojs](https://iojs.org)
```
npm install iojs -g
```
  * dc-addons
```
npm install dc-addons --save
```

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/server/dc-server-chart-with-animations.min.js"></script>
```


## AngularJS Directives
Angular directives for creating charts

#### Usage
Include the angular module `AngularDc`

```js
angular.module('App', ['AngularDc']);
```

Create the chart. Chart options will be an object of all the charts settings.

```html
<dc-chart
    chart="chartObject"
    type="chartType"
    group="chartGroup"
    options="chartOptions"
></dc-chart>
```

#### Demo
Coming soon...


#### Requirements
  * [AngularJS](https://angularjs.org/)
```
bower install angularjs --save
```

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/angular/angular-dc.min.js"></script>
```

## Crossfilter Server
A shell for crossfilter to allow all calculations to happen on the server.

#### Usage

If the normal crossfilter library is not included, this library will take the crossfilter namespace.

```js
    chart.dimension(crossfilterServer.dimension);
    chart.group(crossfilterServer.group(function(filters, chartId, callback) {
        // send a request to the server and return the data in the callback
        ajax(function(response) {
            callback(data);
        });
    }));
```

#### Demo
You will need to clone and run the server locally for an example


#### Requirements
None

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/crossfilter-server/crossfilter-server.min.js"></script>
```

## Crossfilter Server With Elastic Search
Helper functions to integration dc.js charts with elastic search.

#### Usage

If the normal crossfilter library is not included, this library will take the crossfilter namespace.

```js
    var query = {
        aggs: {
            date: {
                date_histogram: {
                    field: 'date_field',
                    interval: '1d',
                }
            },
            site: {
                histogram: {
                    field: 'site_id',
                    interval: 1,
                }
            }
        }
    };
    // when filtering a chart, the chart with the integer id will filter the values base on the given field
    var mapping = {
        1: 'date_field',
        2: 'site_id',
    };

    var url = 'http://localhost:9200/_search';

    chart.dimension(crossfilterServer.dimension);
    chart.group(crossfilterServer.group(function(filters, chartId, callback) {
        // send a request to the server and return the data in the callback
        crossfilterServer.elasticSearch.send(filters, chartId, url, query, mapping, function(data) {
            callback(data.aggregations.date.buckets);
        });
    }));
```

#### Demo
You will need to clone and run the server locally for an example


#### Requirements
None

If you want to include individually
```html
<script src="bower_components/dc-addons/dist/crossfilter-server/crossfilter-server.min.js"></script>
<script src="bower_components/dc-addons/dist/elastic-search/elastic-search.min.js"></script>
```
