#!/usr/bin/env python3
# -*- coding: utf-8 -*-"
import json

class Page(object):
    """Class to represent one HTML page in which the graphs will reside.

    """

    def __init__(self, title_text, heading_text, html_filename):

        self.title_text = title_text
        self.heading_text = heading_text
        self.html_filename = html_filename
        self.charts = []

    @staticmethod
    def _get_header_text():
        """Create the HTML file segment before the graphs.
        
        Returns:
            string: The HTML text to go before the graphs.

        """

        header_text  = '<!DOCTYPE html>\n'
        header_text += '<html>\n'
        header_text += '<head>\n'
        header_text += '<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n'
        header_text += '<script src="http://code.highcharts.com/highcharts.js"></script>\n'
        header_text += '</head>\n'
        header_text += '<body>\n'

        return header_text

    @staticmethod
    def _get_footer_text():
        """Create the HTML file segment at the end after the graphs

        Returns:
            string: The HTML text to go at the end after the graphs.

        """

        footer_text  = '\n\n</body>\n\n'
        footer_text  = '</html>'

        return footer_text

    def add_chart(self, chart):
        """Add a chart to the list of charts in this page

        Args:
            chart (Chart): A full created Chart instance.

        """

        self.charts.append(chart)

    def to_html(self):
        """Create the HTML text that can be viewed in a browser.

        Returns:
            string: HTML text to display in a browser.

        """

        indent = '  '

        html_text = Page._get_header_text()

        for index, chart in enumerate(self.charts):
            html_text += '  <div id="container%d" style="display:block; margin-left:auto;margin-right: auto; width:800px; height:400px;"></div>\n'%index
            html_text += Page._indent(2, "<script>\n")
            html_text += Page._indent(4,'$(function () {\n')
            html_text += Page._indent(6,'$("#container%d").highcharts(\n'%index)
            for line in chart.to_json_string().split('\n'):
                html_text += Page._indent(8, line)
                html_text += '\n'
            html_text += Page._indent(4, ');\n')
            html_text += Page._indent(4, '});\n')
            html_text += Page._indent(2, "</script>\n")

        html_text += Page._get_footer_text()

        return html_text

    @staticmethod
    def _indent(num_spaces, text):
        indented_string = ""
        spaces_list = list()
        for indent in range(0, num_spaces):
            spaces_list.append(' ')
        return ''.join(spaces_list) + text


class Chart(object):

    def __init__(self):
        self._chart = {}
        self._set_defaults()

    def _set_defaults(self):
        self.set_credits()
        self.set_chart()
        self.set_title()
        self.set_subtitle()
        self.set_xaxis()
        self.set_yaxis()
        self.set_tooltip()
        self.set_plot_options()

    def set_chart(self, chart_type='line', zoom_type='x'):
        if chart_type is None:
            self._chart.pop('chart', None)
        self._chart['chart'] = { 'type' : chart_type, 'zoomType' : zoom_type }

    def set_credits(self, text='jrtools', href='http://github.com/jrseti/jrtools'):
        self._chart['credits'] = { 'text' : text, 'href' : href }

    def set_title(self, title='Chart Title'):
        self._chart['title'] = { 'text' : title } 

    def set_subtitle(self, subtitle=None):
        if subtitle is None:
            self._chart.pop('subtitle', None)
            return
        self._chart['subtitle'] = { 'text' : subtitle } 

    def set_xaxis(self, axis_type='linear', text='Need to set X axis text'):
        #if axis_type is not 'xx':
        #    raise Exception('axis_type %s not valid. Valid types are linear, scatter, datetime')
        self._chart['xAxis'] = dict()
        self._chart['xAxis']['type'] = axis_type
        self._chart['xAxis']['title'] = dict()
        self._chart['xAxis']['title']['text'] = text

    def set_yaxis(self, axis_type='linear', text='Need to set Y axis text'):
        self._chart['yAxis'] = dict()
        self._chart['yAxis']['type'] = axis_type
        self._chart['yAxis']['title'] = dict()
        self._chart['yAxis']['title']['text'] = text

    def set_tooltip(self, tooltip_dict=None):
        if tooltip_dict is None:
            self._chart.pop('tooltip', None)
            return
        self._chart['tooltip'] = tooltip_dict

    def set_plot_options(self, plot_options_dict=None):
        if plot_options_dict is None:
            self._chart.pop('plotOptions', None)
            return
        self._chart['plotOptions'] = plot_options_dict

    def add_series(self, series):
        series_list = self._chart.get('series', list())
        series_list.append(series.get())
        self._chart['series'] = series_list

    def to_json_string(self, insert_newlines=False):
        if 'series' in self._chart:
            json_string = json.dumps(self._chart, indent=2)
            return json_string
        raise Exception('The series has not been defined. Cannot create a valid chart.')

class Series:

    def __init__(self, name, data, marker=None):
        self._series = dict()
        self._series['name'] = name
        self._series['data'] = data
        if marker is not None:
            self._series['marker'] = marker

    def set_type(series_type):
        self._series['type'] = series_type

    def get(self):
        return self._series


data = [[1,1],[2,2],[3,3]]
marker = { 'marker' : { 'symbol' : 'circle', 'radius' : 0 } }
series = Series('test series', data, marker)
chart = Chart()
chart.set_title("My First Chart")
chart.add_series(series)
page = Page('Chart Test', 'This is my chart test', 'chart_test1.html')
page.add_chart(chart)
page.add_chart(chart)
print(page.to_html())
