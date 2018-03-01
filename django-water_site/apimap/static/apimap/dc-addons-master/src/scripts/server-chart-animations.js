(function () {
    'use strict';

    if (dc.serverChart.redrawPieChart) {
        return false;
    }

    var duration = 5000;
    var ease = 'quad-in-out';
    var pieRegEx = new RegExp([
        'M ?([\\d\\.e-]+) ?, ?([\\d\\.e-]+) ?', // move to starting point
        // see https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#Arcs
        'A ?', // start arc
            '[\\d\\.e-]+ ?, ?[\\d\\.e-]+ ?,? ', // arc x radius and y radius
            '\\d ,? ?', // arc x-axis-rotation
            '\\d ?,? ?', // arc large-arc-flag
            '\\d ?,? ?', // arc sweep-flag
            '([\\d\\.e-]+) ?,? ?([\\d\\.e-]+) ?', // arc finishing points
        'L ?([\\d\\.e-]+) ?,? ?([\\d\\.e-]+)', // draw line too
        'Z', // close off
    ].join(''));

    dc.serverChart.redrawPieChart = function (chartIndex, chartWrapper, nextWrapper) {
        var svg = chartWrapper.select('svg'),
            currentSlices = chartWrapper.selectAll('g.pie-slice'),
            nextSlices = nextWrapper.selectAll('g.pie-slice');

        chartWrapper
            .select('g')
            .attr('class', nextWrapper.select('g').attr('class'));

        chartWrapper
            .selectAll('text')
            .each(function (textData, textIndex) {
                var textElement = d3.select(this),
                    nextText = filterNextItem(nextWrapper.selectAll('text'), textIndex);

                if (nextText.empty()) {
                    textElement
                        .text('');
                } else {
                    textElement
                        .text(nextText.text())
                        .transition()
                            .duration(duration)
                            .ease(ease)
                            .attr('transform', nextText.attr('transform'));
                }
            });

        currentSlices
            .each(function (sliceData, sliceIndex) {
                var sliceElement = d3.select(this),
                    nextSlice = filterNextItem(nextSlices, sliceIndex);

                if (!nextSlice.empty()) {
                    sliceElement
                        .attr('class', nextSlice.attr('class'));

                    var nextText = nextSlice.select('text');

                    if (!nextText.empty()) {
                        sliceElement
                            .select('title')
                            .text(nextText.text());
                    }
                }
            });

        currentSlices
            .select('path')
            .each(function (sliceData, sliceIndex) {
                var sliceElement = d3.select(this),
                    nextSlice = filterNextItem(nextSlices, sliceIndex).select('path');

                if (!nextSlice.empty()) {
                    sliceElement
                        .attr('class', nextSlice.attr('class'))
                        .attr('fill', nextSlice.attr('fill'));
                }
            })
            .transition()
                .duration(duration)
                .ease(ease)
                .attrTween('d', function (pathData, pathIndex, attrValue) {
                    var radius = d3.min([svg.attr('width'), svg.attr('height')]) / 2,
                        arc = d3.svg.arc().outerRadius(radius).innerRadius(0),
                        nextSlice = filterNextItem(nextSlices, pathIndex),
                        nextD = '';

                    if (!nextSlice.empty()) {
                        nextD = nextSlice.select('path').attr('d');
                    }

                    var interpolate = d3.interpolate(
                            pathToInterpolateAngles(attrValue),
                            pathToInterpolateAngles(nextD)
                        );

                    return function (t) {
                        return arc(interpolate(t));
                    };
                });
    };

    dc.serverChart.redrawBarChart = function (chartIndex, chartWrapper, nextWrapper) {
        var currentBars = chartWrapper.selectAll('rect.bar'),
            nextBars = nextWrapper.selectAll('rect.bar');

        currentBars
            .each(function (barData, barIndex) {
                var barElement = d3.select(this),
                    nextBar = filterNextItem(nextBars, barIndex);

                barElement
                    .attr('class', nextBar.attr('class'))
                    .attr('fill', nextBar.attr('fill'))
                    .transition()
                        .duration(duration)
                        .ease(ease)
                        .attr('x', nextBar.attr('x'))
                        .attr('y', nextBar.attr('y'))
                        .attr('width', nextBar.attr('width'))
                        .attr('height', nextBar.attr('height'));
            });

        currentBars
            .select('title')
            .each(function (titleData, titleIndex) {
                var titleElement = d3.select(this),
                    nextTitle = filterNextItem(nextBars, titleIndex).select('title');

                titleElement
                    .text(nextTitle.text());
            });

        redrawAxis(chartIndex, chartWrapper, nextWrapper);
    };

    dc.serverChart.redrawRowChart = dc.serverChart.redrawPairedRowChart = function (chartIndex, chartWrapper, nextWrapper) {
        chartWrapper
            .selectAll('g.row')
            .each(function (rowData, rowIndex) {
                var rowElement = d3.select(this),
                    nextRow = filterNextItem(nextWrapper.selectAll('g.row'), rowIndex),
                    nextRect = nextRow.select('rect'),
                    nextText = nextRow.select('text'),
                    nextTitle = nextRow.select('title');

                rowElement
                    .transition()
                    .duration(duration)
                    .ease(ease)
                    .attr('transform', nextRow.attr('transform'));

                rowElement
                    .select('rect')
                    .attr('class', nextRect.attr('class'))
                    .transition()
                        .duration(duration)
                        .ease(ease)
                        .attr('width', nextRect.attr('width'))
                        .attr('height', nextRect.attr('height'))
                        .attr('fill', nextRect.attr('fill'))
                        .attr('transform', nextRect.attr('transform'));

                rowElement
                    .select('text')
                    .text(nextText.text())
                    .transition()
                        .duration(duration)
                        .ease(ease)
                        .attr('x', nextText.attr('x'))
                        .attr('y', nextText.attr('y'))
                        .attr('dy', nextText.attr('dy'))
                        .attr('transform', nextText.attr('transform'));

                rowElement
                    .select('title')
                    .text(nextTitle.text());
            });

        redrawAxis(chartIndex, chartWrapper, nextWrapper);
    };

    dc.serverChart.redrawLineChart = function (chartIndex, chartWrapper, nextWrapper) {
        chartWrapper
            .selectAll('g.stack')
            .each(function (stackData, stackIndex) {
                var stackElement = d3.select(this),
                    nextStack = filterNextItem(nextWrapper.selectAll('g.stack'), stackIndex);

                stackElement
                    .selectAll('path')
                    .each(function (pathData, pathIndex) {
                        var pathElement = d3.select(this),
                            nextPath = filterNextItem(nextStack.selectAll('path'), pathIndex);

                        pathElement
                            .transition()
                                .duration(duration)
                                .ease(ease)
                                .attr('stroke', nextPath.attr('stroke'))
                                .attr('d', nextPath.attr('d'));
                    });
            });

        redrawAxis(chartIndex, chartWrapper, nextWrapper);
    };

    dc.serverChart.redrawNumberDisplay = function (chartIndex, chartWrapper, nextWrapper) {
        var spanElement = chartWrapper.select('span.number-display'),
            spanText = spanElement.text(),
            textParts = spanText.match(/([^\d]*)([\d\.]+)([^\d]*)/i),
            currentNumber = textParts === null ? 0 : parseFloat(textParts[2]),
            nextSpan = nextWrapper.select('span.number-display'),
            nextText = nextSpan.text(),
            nextParts = nextText.match(/([^\d]*)([\d\.]+)([^\d]*)/i),
            nextNumber = nextParts === null ? 0 : parseFloat(nextParts[2]);

        spanElement.transition()
            .duration(duration)
            .ease(ease)
            .tween('text', function () {
                var interp = d3.interpolateNumber(currentNumber, nextNumber);
                return function (t) {
                    var num = d3.format('.2s')(interp(t));
                    this.innerHTML = nextParts[1] + num + nextParts[3];
                };
            });
    };

    function redrawAxis (chartIndex, chartWrapper, nextWrapper) {
        chartWrapper
            .selectAll('.axis')
            .each(function (axisData, axisIndex) {
                var axisElement = d3.select(this),
                    axisBBox = axisElement.select('path.domain').node().getBBox(),
                    axisTicks = axisElement.selectAll('g.tick'),
                    isHorizontal = axisTicks.empty() ? null : /translate\([\d.]+,0\)/i.exec(d3.select(axisTicks[0][1]).attr('transform')) !== null,
                    firstRow = d3.select(axisElement[0][0].nextElementSibling),
                    isRightYAxis = firstRow.empty() ? null : /translate\(0,[\d.]+\)/i.exec(firstRow.attr('transform')) === null,
                    nextAxis = filterNextItem(nextWrapper.selectAll('.axis'), axisIndex),
                    nextTicks = nextAxis.selectAll('g.tick'),
                    minTickValue = nextTicks.empty() ? 0 : parseFloat(d3.select(nextTicks[0][0]).select('text').text()),
                    maxTickValue = nextTicks.empty() ? 1 : parseFloat(d3.select(nextTicks[0][nextTicks[0].length - 1]).select('text').text()),
                    grid = chartWrapper.select(isHorizontal ? '.grid-line.vertical' : '.grid-line.horizontal'),
                    nextGrid = nextWrapper.select(isHorizontal ? '.grid-line.vertical' : '.grid-line.horizontal');

                axisElement
                    .transition()
                        .duration(duration)
                        .ease(ease)
                        .attr('transform', nextAxis.attr('transform'));

                if (!grid.empty()) {
                    grid
                        .transition()
                            .duration(duration)
                            .ease(ease)
                            .attr('transform', nextGrid.attr('transform'));
                }

                axisTicks
                    .each(function (tickData, tickIndex) {
                        var tickElement = d3.select(this),
                            tickText = tickElement.select('text'),
                            tickValue = parseFloat(tickText.text()),
                            tickPercentage = (tickValue - minTickValue) / (maxTickValue - minTickValue) * 100,
                            matched = false;

                        nextTicks
                            .each(function (nextData, nextIndex) {
                                var nextTick = d3.select(this),
                                    nextText = nextTick.select('text');

                                if (parseFloat(nextText.text()) === tickValue) {
                                    matched = true;

                                    tickElement
                                        .transition()
                                            .duration(duration)
                                            .ease(ease)
                                            .attr('transform', nextTick.attr('transform'))
                                            .attr('opacity', null)
                                            .style('opacity', nextTick.attr('opacity'))
                                        .each('end', function () {
                                            tickElement
                                                .select('text')
                                                .text(nextTick.select('text').text());
                                        });

                                    if (!grid.empty()) {
                                        var gridLine = filterNextItem(grid.selectAll('line'), tickIndex),
                                            nextGridLine = filterNextItem(nextGrid.selectAll('line'), nextIndex);

                                        gridLine
                                            .transition()
                                                .duration(duration)
                                                .ease(ease)
                                                .attr('x1', nextGridLine.attr('x1'))
                                                .attr('y1', nextGridLine.attr('y1'))
                                                .attr('x2', nextGridLine.attr('x2'))
                                                .attr('y2', nextGridLine.attr('y2'))
                                                .attr('transform', null)
                                                .style('opacity', nextGridLine.attr('opacity'));
                                    }

                                }
                            });

                        if (!matched) {
                            var transform = '';

                            if (isHorizontal) {
                                var translate = (axisBBox.width * tickPercentage / 100);
                                if (isRightYAxis) {
                                    transform = 'translate(-' + translate + ', 0)';
                                } else {
                                    transform = 'translate(' + translate + ', 0)';
                                }
                            } else {
                                transform = 'translate(0, ' +
                                    (axisBBox.height - (axisBBox.height * tickPercentage / 100)) +
                                ')';
                            }

                            tickElement
                                .transition()
                                    .duration(duration)
                                    .ease(ease)
                                    .attr('transform', transform)
                                    .style('opacity', 0)
                                .each('end', function () {
                                    tickElement.remove();
                                });

                            if (!grid.empty()) {
                                var gridLine = filterNextItem(grid.selectAll('line'), tickIndex);

                                gridLine
                                    .transition()
                                        .duration(duration)
                                        .ease(ease)
                                        .attr('transform', transform)
                                        .style('opacity', 0)
                                    .each('end', function () {
                                        gridLine.remove();
                                    });
                            }
                        }
                    });
            });

        nextWrapper
            .selectAll('.axis')
            .each(function (d, axisIndex, tickIndex) {
                var nextAxis = d3.select(this),
                    nextTicks = nextAxis.selectAll('g.tick');

                if (!nextTicks.empty()) {
                    var isHorizontal = /translate\([\d.]+,0\)/i.exec(d3.select(nextTicks[0][1]).attr('transform')) !== null,
                        firstRow = d3.select(nextAxis[0][0].nextElementSibling),
                        isRightYAxis = firstRow.empty() ? null : /translate\(0,[\d.]+\)/i.exec(firstRow.attr('transform')) === null,
                        axisElement = filterNextItem(chartWrapper.selectAll('.axis'), axisIndex),
                        axisBBox = axisElement.select('path.domain').node().getBBox(),
                        axisTicks = axisElement.selectAll('g.tick'),
                        minTickValue = axisTicks.empty() ? 0 : parseFloat(d3.select(axisTicks[0][0]).select('text').text()),
                        maxTickValue = axisTicks.empty() ? 1 : parseFloat(d3.select(axisTicks[0][axisTicks[0].length - 1]).select('text').text()),
                        grid = chartWrapper.select(isHorizontal ? '.grid-line.vertical' : '.grid-line.horizontal'),
                        nextGrid = nextWrapper.select(isHorizontal ? '.grid-line.vertical' : '.grid-line.horizontal');

                    nextTicks
                        .each(function (nextData, nextIndex) {
                            var nextTick = d3.select(this),
                                nextText = nextTick.select('text'),
                                nextLine = nextTick.select('line'),
                                nextValue = parseFloat(nextText.text()),
                                tickPercentage = (nextValue - minTickValue) / (maxTickValue - minTickValue) * 100,
                                matched = false;

                            axisTicks
                                .each(function (tickData, tickIndex) {
                                    var tickElement = d3.select(this),
                                        tickText = tickElement.select('text');

                                    if (parseFloat(tickText.text()) === nextValue) {
                                        matched = true;
                                    }
                                });

                            if (!matched) {
                                var translate = 0,
                                    transform = '',
                                    gridLineTransform = '',
                                    nextGridLine = null;

                                if (grid.empty()) {
                                    nextGridLine = nextTick.select('line.grid-line');
                                } else {
                                    nextGridLine = filterNextItem(nextGrid.selectAll('line'), nextIndex);
                                }

                                if (isHorizontal) {
                                    translate = axisBBox.width * tickPercentage / 100;

                                    if (isRightYAxis) {
                                        transform = 'translate(-' + translate + ', 0)';
                                    } else {
                                        transform = 'translate(' + translate + ', 0)';
                                    }

                                    if (!nextGridLine.empty()) {
                                        gridLineTransform = 'translate(' + (translate - nextGridLine.attr('x1')) + ', 0)';
                                    }
                                } else {
                                    translate = axisBBox.height - (axisBBox.height * tickPercentage / 100);
                                    transform = 'translate(0, ' + translate + ')';

                                    if (!nextGridLine.empty()) {
                                        gridLineTransform = 'translate(0, ' + (translate - nextGridLine.attr('y1')) + ')';
                                    }
                                }

                                var addedTick = axisElement
                                    .append('g')
                                    .attr('class', 'tick')
                                    .attr('transform', transform)
                                    .attr('opacity', 0);

                                addedTick
                                    .transition()
                                        .duration(duration)
                                        .ease(ease)
                                        .attr('transform', nextTick.attr('transform'))
                                        .style('opacity', 1);

                                addedTick
                                    .append('text')
                                    .attr('x', nextText.attr('x'))
                                    .attr('y', nextText.attr('y'))
                                    .attr('dy', nextText.attr('dy'))
                                    .attr('style', nextText.attr('style'))
                                    .text(nextText.text());

                                addedTick
                                    .append('line')
                                    .attr('x1', nextLine.attr('x1'))
                                    .attr('y1', nextLine.attr('y1'))
                                    .attr('x2', nextLine.attr('x2'))
                                    .attr('y2', nextLine.attr('y2'));

                                if (!nextGridLine.empty()) {
                                    if (grid.empty()) {
                                        addedTick
                                            .append('line')
                                            .attr('class', nextGridLine.attr('class'))
                                            .attr('x1', nextGridLine.attr('x1'))
                                            .attr('y1', nextGridLine.attr('y1'))
                                            .attr('x2', nextGridLine.attr('x2'))
                                            .attr('y2', nextGridLine.attr('y2'));
                                    } else {
                                        grid
                                            .append('line')
                                            .attr('x1', nextGridLine.attr('x1'))
                                            .attr('y1', nextGridLine.attr('y1'))
                                            .attr('x2', nextGridLine.attr('x2'))
                                            .attr('y2', nextGridLine.attr('y2'))
                                            .attr('transform', gridLineTransform)
                                            .attr('opacity', 0)
                                            .transition()
                                                .duration(duration)
                                                .ease(ease)
                                                .attr('transform', 'translate(0, 0)')
                                                .style('opacity', 1);
                                    }
                                }
                            }
                        });
                }
            });
    }

    function filterNextItem (next, i) {
        return next.filter(function (d, j) {
            return j === i;
        });
    }

    function pathToInterpolateAngles(path) {
        // get the points of the pie slice
        var p = path.match(pieRegEx);

        if (!p) {
            return {
                startAngle: 0,
                endAngle: Math.PI * 2,
            };
        }

        var coords = {
            x1: parseFloat(p[5]),
            y1: parseFloat(p[6]),
            x2: parseFloat(p[1]),
            y2: parseFloat(p[2]),
            x3: parseFloat(p[3]),
            y3: parseFloat(p[4]),
        };

        // convert the points into angles
        var angles = {
            startAngle: switchRadians(Math.atan2((coords.y2 - coords.y1), (coords.x2 - coords.x1))),
            endAngle:   switchRadians(Math.atan2((coords.y3 - coords.y1), (coords.x3 - coords.x1))),
        };

        if (angles.startAngle < 0) {
            angles.startAngle = 0;
        }

        if (angles.endAngle > (Math.PI * 2) || angles.endAngle < angles.startAngle) {
            angles.endAngle = Math.PI * 2;
        }

        return angles;
    }

    // since silly maths makes the following angles we have to convert it from
    //      -90               -(PI / 2)
    // -180     0   or    -PI             0
    //       90                  PI / 2
    //
    // to
    //
    //     360                   PI * 2
    // 270     90   or    PI * 1.5     PI / 2
    //     180                      PI
    function switchRadians(angle) {
        var quarter     = Math.PI * 0.5;

        if (angle >= 0) {
            return quarter + angle;
        } else if (angle >= -quarter) {
            return quarter - Math.abs(angle);
        }

        return (Math.PI * 2.5) - Math.abs(angle);
    }
})();
