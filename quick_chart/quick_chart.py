#!/usr/bin/env python3
# -*- coding: utf-8 -*-"

#CHART_TEMPLATE = {
#        chart: {
#            type: 'spline'
#            },
#        credits: {
#            text: 'jrseti',
#            href: 'https://github.com/jrseti/jrtools'
#            },
#        title: {
#            text: ''
#            },
#        subtitle: {
#            text: 'Based on Perley and Butler, 2016: https://arxiv.org/pdf/1609.05940.pdf'
#            },
#        xAxis: {
#            type:'logarithmic',
#            title: {
#                text: 'Frequency in GHz'
#                }
#            },
#        yAxis: {
#            type:'logarithmic',
#            title: {
#                text: 'Jy'
#                },
#            labels: {
#                formatter: function () {
#                    return this.value;
#                    }
#                }
#            },
#        tooltip: {
#            crosshairs: true,
#            shared: true,
#            headerFormat: '{point.x:.3f} GHz<br>',
#            pointFormat: '{point.y} Jy',
#            },
#        plotOptions: {
#            spline: {
#                marker: {
#                    radius: 0,
#                    lineColor: '#666666',
#                    lineWidth: 1
#                    }
#                }
#            },
#        series: [{
#            name: 'Flux Density of $source',
#            marker: {
#                symbol: 'square'
#                },
#            data: $data
#            }]
#        }

import json

class Page(object):
    """Class to represent one HTML page in which the graphs will reside.

    """

    def __init__(self, title_text, heading_text, html_filename):

        self.title_text = title_text
        self.heading_text = heading_text
        self.html_filename = html_filename
        self.charts = []

    def _get_header_text():
        """Create the HTML file segment before the graphs.
        
        Returns:
            string: The HTML text to go before the graphs.

        """

        header_text  = '<!DOCTYPE html>\n'
        header_text += '<html>\n'
        header_text += '<head>\n'
        header_text += '<script src="http://ajax.googleapis.com/ajax/libs/\
                        jquery/1.8.2/jquery.min.js"></script>\n'
        header_text += '<script src="http://code.highcharts.com/highcharts.js"\
                        ></script>\n'
        header_text += '</head>\n'
        header_text += '<body>\n'

        return header_text

    def _get_footer_text():
        """Create the HTML file segment at the end after the graphs

        Returns:
            string: The HTML text to go at the end after the graphs.

        """

        footer_text  = '\n\n</body>\n\n'
        footer_text  = '</html>'

        return footer_text

    def add_chart(chart):
        """Add a chart to the list of charts in this page

        Args:
            chart (Chart): A full created Chart instance.

        """

        self.charts.append(chart)

    def to_html():
        """Create the HTML text that can be viewed in a browser.

        Returns:
            string: HTML text to display in a browser.

        """

        html_text = _get_header_text()

        for graph in self.graphs:
            html_text += graph.to_javasctipt_text()

        html_text += _get_footer_text()

        return html_text


class Chart:


    def __init__(self, title, chart_type, series_list, **kwargs=None):

        self.chart = {}

        self.set_title(title)
        self.set_series(series_list)
        self.set_chart_type(chart_type)

        if kwargs is not None:
            self.set_credits(kwargs.get('credits', None))
            self.set_subtitle(kwargs.get('subtitle', None))
            self.set_xaxis(kwargs.get('xaxis', None))

    def toJSON(self):
        return json.dumps(self.chart)

    def set_title(self, title_text):
        self.chart['title'] = { 'text' : title_text } 

    def set_series(self, series_list):
        self.chart['series'] = series_list 

    def set_chart_type(self, chart_type):
        self.chart['chart'] = { 'type' : chart_type }

    def set_credits(self, credits):
        if credits is None:
            self.chart['credits'] = { 'text' : 'jrtools', 'href' : 'http://github.com/jrseti/jrtools' } 
            return
        self.chart['credits'] = credits

    def set_subtitle(self, subtitle):
        if subtitle is None:
            return
        self.chart['subtitle'] = { 'text' : subtitle } 

    def set_xaxis(self, xaxis):
        if xaxis is None:
            self.chart['xAxis'] = { 'type' : 'datetime', 'title' : 'X Axis' } 
            return
        self.chart['xAxis'] = xaxis

series = [{ 'name' : 'test series', 'data' : [1,2,3]}]

kwargs = {}
kwargs['chart'] = { 'type' : 'scatter' }
kwargs['credits'] = { 'text' : 'These are the credits' }
kwargs['subtitle'] = 'This is a subtitle'
kwargs['xaxis'] = {"type": "datetime", "title": "This is the X Axis"}
chart = QuickChart('Test Title', 'scatter', series,  **kwargs)
print(chart.toJSON())
