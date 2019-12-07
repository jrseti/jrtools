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

import hjson

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


    def __init__(self, title, chart_type, series_list, **kwargs):

        self.chart = {}

        self.chart['chart'] = { 'type' : chart_type }
        self.chart['title'] = { 'text' : title }
        self.chart['series'] = series_list

        for key, value in kwargs.items():
            self.chart[key] = value

    def _set_defaults():
        self.chart['credits'] = { 'text' : 'jrtools', 'href' : 'http://github.com/jrseti/jrtools' }
        self.chart['xAxis'] = { 'type' : 'datetime', 'title' : 'X Axis' }

    def set_credits(self, credits):
        self.chart['credits'] = credits

    def set_subtitle(self, subtitle):
        self.chart['subtitle'] = { 'text' : subtitle } 

    def set_xaxis(self, xaxis):
        self.chart['xAxis'] = xaxis

    def toJSON(self, insert_newlines=False):
        json_string = json.dumps(self.chart, indent=2)
        return json_string

series = [{ 'name' : 'test series', 'data' : [1,2,3]}]

chart = Chart('Test Title', 'scatter', series )
print(chart.toJSON())
