(function () {
    'use strict';

    if (dc.baseGoogleChart) {
        return false;
    }

    dc.baseGoogleChart = function (_chart) {
        _chart = dc.baseMapChart(_chart);

        _chart._doRender = function () {
            var _map = new google.maps.Map(_chart.root().node(), _chart.mapOptions());

            if (_chart.center() && _chart.zoom()) {
                _map.setCenter(_chart.toLocArray(_chart.center()));
                _map.setZoom(_chart.zoom());
            }

            _chart.map(_map);

            _chart._postRender();

            return _chart._doRedraw();
        };

        _chart.toLocArray = function (value) {
            if (typeof value === 'string') {
                // expects '11.111,1.111'
                value = value.split(',');
            }

            // else expects [11.111,1.111]
            return new google.maps.LatLng(value[0], value[1]);
        };

        return _chart;
    };
})();
