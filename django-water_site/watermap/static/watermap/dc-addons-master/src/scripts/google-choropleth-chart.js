(function () {
    'use strict';

    if (dc.googleChoroplethChart) {
        return false;
    }

    dc.googleChoroplethChart = function (parent, chartGroup) {
        var _chart = dc.colorChart(dc.baseGoogleChart({}));

        var _dataMap = [];

        var _geojson = false;
        var _feature = false;
        var _featureOptions = {
            fillColor: 'black',
            color: 'gray',
            opacity: 0.4,
            fillOpacity: 0.6,
            weight: 1
        };
        var _infoWindow = null;

        var _featureKey = function (feature) {
            return feature.key;
        };

        var _featureStyle = function (feature) {
            var options = _chart.featureOptions();
            if (options instanceof Function) {
                options = options(feature);
            }
            options = JSON.parse(JSON.stringify(options));
            var v = _dataMap[_chart.featureKeyAccessor()(feature)];
            if (v && v.d) {
                options.fillColor = _chart.getColor(v.d, v.i);
                if (_chart.filters().indexOf(v.d.key) !== -1) {
                    options.opacity = 0.8;
                    options.fillOpacity = 1;
                }
            }
            return options;
        };

        _chart._postRender = function () {
            if (typeof _geojson === 'string') {
                _feature = _chart.map().data.loadGeoJson(_geojson);
            } else {
                _feature = _chart.map().data.addGeoJson(_geojson);
            }

            _chart.map().data.setStyle(_chart.featureStyle());
            processFeatures();
        };

        _chart._doRedraw = function () {
            _dataMap = [];
            _chart._computeOrderedGroups(_chart.data()).forEach(function (d, i) {
                _dataMap[_chart.keyAccessor()(d)] = {d: d, i: i};
            });
            _chart.map().data.setStyle(_chart.featureStyle());
        };

        _chart.geojson = function (_) {
            if (!arguments.length) {
                return _geojson;
            }

            _geojson = _;
            return _chart;
        };

        _chart.featureOptions = function (_) {
            if (!arguments.length) {
                return _featureOptions;
            }

            _featureOptions = _;
            return _chart;
        };

        _chart.featureKeyAccessor = function (_) {
            if (!arguments.length) {
                return _featureKey;
            }

            _featureKey = _;
            return _chart;
        };

        _chart.featureStyle = function (_) {
            if (!arguments.length) {
                return _featureStyle;
            }

            _featureStyle = _;
            return _chart;
        };

        var processFeatures = function (feature, layer) {
            if (_chart.renderPopup()) {
                _chart.map().data.addListener('click', function (event) {
                    var anchor = new google.maps.MVCObject(),
                        data = _dataMap[_chart.featureKeyAccessor()(event.feature)];

                    if (_infoWindow) {
                        _infoWindow.close();
                    }

                    if (!data) {
                        data = {};
                    }

                    if (!data.d) {
                        data.d = {};
                    }

                    _infoWindow = new google.maps.InfoWindow({
                        content: _chart.popup()(data.d, event.feature)
                    });

                    anchor.set('position', event.latLng);
                    _infoWindow.open(_chart.map(), anchor);
                });
            }

            if (_chart.brushOn()) {
                _chart.map().data.addListener('click', selectFilter);
            }
        };

        var selectFilter = function (event) {
            if (!event.feature) {
                return;
            }

            var filter = _chart.featureKeyAccessor()(event.feature);

            dc.events.trigger(function () {
                _chart.filter(filter);
                dc.redrawAll(_chart.chartGroup());
            });
        };

        return _chart.anchor(parent, chartGroup);
    };
})();
