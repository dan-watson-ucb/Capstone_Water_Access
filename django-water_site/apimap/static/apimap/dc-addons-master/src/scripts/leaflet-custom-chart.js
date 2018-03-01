(function () {
    'use strict';

    if (dc.leafletCustomChart) {
        return false;
    }

    dc.leafletCustomChart = function (parent, chartGroup) {
        var _chart = dc.baseLeafletChart({});

        var _redrawItem = null;
        var _renderItem = null;

        _chart.renderTitle(true);

        _chart._postRender = function () {
            var data = _chart._computeOrderedGroups(_chart.data());

            data.forEach(function (d, i) {
                _chart.renderItem()(_chart, _chart.map(), d, i);
            });
        };

        _chart._doRedraw = function () {
            var data = _chart._computeOrderedGroups(_chart.data());

            var accessor = _chart.valueAccessor();

            data.forEach(function (d, i) {
                d.filtered = accessor(d) === 0;
                _chart.redrawItem()(_chart, _chart.map(), d, i);
            });
        };

        _chart.redrawItem = function (_) {
            if (!arguments.length) {
                return _redrawItem;
            }

            _redrawItem = _;
            return _chart;
        };

        _chart.renderItem = function (_) {
            if (!arguments.length) {
                return _renderItem;
            }

            _renderItem = _;
            return _chart;
        };

        return _chart.anchor(parent, chartGroup);
    };
})();
