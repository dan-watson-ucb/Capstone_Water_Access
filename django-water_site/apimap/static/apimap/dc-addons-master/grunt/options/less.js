module.exports = function () {
    return {
        options: {
            strictMath: true,
        },
        tooltip: {
            dest: '<%= config.dist %>/tooltip/dc-tooltip-mixin.css',
            src: [
                '<%= config.src %>/<%= config.less %>/tooltip-mixin.less'
            ]
        },
        leaflet: {
            dest: '<%= config.dist %>/leaflet-map/dc-leaflet-legend.css',
            src: [
                '<%= config.src %>/<%= config.less %>/leaflet-legend.less'
            ]
        },
        hexbin: {
            dest: '<%= config.dist %>/hexbin/dc-hexbin-chart.css',
            src: [
                '<%= config.src %>/<%= config.less %>/hexbin-chart.less',
            ]
        },
        build: {
            dest: '<%= config.dist %>/dc-addons.css',
            src: [
                '<%= config.src %>/<%= config.less %>/tooltip-mixin.less',
                '<%= config.src %>/<%= config.less %>/leaflet-legend.less',
                '<%= config.src %>/<%= config.less %>/hexbin-chart.less',
            ]
        },
    };
};
