(function () {
    'use strict';

    var dcServerChart = function () {
        return {
            restrict: 'E',
            scope: {
                options: '=',
                conditions: '=',
            },
            link: function ($scope, element) {
                var chart = dc.serverChart(element[0]),
                    hasInit = false;

                $scope.$watch('options', function () {
                    if (!hasInit && $scope.options) {
                        chart.options($scope.options).render();
                        hasInit = true;
                    }
                });

                $scope.$watch('conditions', function () {
                    if ($scope.conditions) {
                        chart.conditions($scope.conditions);
                    }
                });
            }
        };
    };

    dcServerChart.$inject = [];

    angular.module('AngularDc').directive('dcServerChart', dcServerChart);

})();
