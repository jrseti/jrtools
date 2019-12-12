#!/usr/bin/env python3
# -*- coding: utf-8 -*-"

"""Creates a chart with your custom data. This charts is in the form of an HTML
   file and requires a browers to view.
   Highcharts (http://highcharts.com) is used as the javascript library to draw
   the chart.

   Example that creates the text of an HTML file containing a chart:

    #Create a Chart object and set the title
    chart = Chart()
    chart.set_title("My First Chart")

    #Create a data series
    data = [[1, 1], [2, 2], [3, 3]]
    marker = {'marker': {'symbol': 'circle', 'radius': 0}}
    series = Series('test series', data, marker)

    #Add the series to the chart
    chart.add_series(series)

    #Create an HTML page object
    page = Page('Chart Test', 'This is my chart test', 'chart_test1.html')

    #Add the chart to the HTML page
    page.add_chart(chart)

    #Output the HTML to a file
    page.to_file("testxx.html")

"""
import copy
import json


class Page():
    """Class to represent one HTML page in which the charts will reside. """

    def __init__(self, title_text, heading_text):
        self.title_text = title_text
        self._heading_text = heading_text
        self._charts = []

    def add_chart(self, new_chart):
        """Add a chart to the list of charts in this page

        Args:
            chart (Chart): A full created Chart instance.

        """

        self._charts.append(new_chart)

    def to_html(self):
        """Create the HTML text that can be viewed in a browser.

        Returns:
            str: HTML text to display in a browser.

        """

        html_text = self._get_header_text()

        for index, chart in enumerate(self._charts):
            html_text += '  <div id="container%d" style="display:block;'\
                         'margin-left:auto;margin-right: auto; width:%dpx;'\
                         'height:%dpx;"></div>\n'%(index, chart.width, chart.height)
            html_text += Page._indent(2, "<script>\n")
            html_text += Page._indent(4, '$(function () {\n')
            html_text += Page._indent(
                6, '$("#container%d").highcharts(\n' % index)
            for line in chart.to_json_string().split('\n'):
                html_text += Page._indent(8, line)
                html_text += '\n'
            html_text += Page._indent(4, ');\n')
            html_text += Page._indent(4, '});\n')
            html_text += Page._indent(2, "</script>\n")

        html_text += Page._get_footer_text()

        return html_text

    def to_file(self, filename):
        """Create the HTML and save to a file.

        Args:
            filename (str): The full path output filename.

        Raises:
            Exception: The result of opening and writing to the file.

        """

        with open(filename, 'w') as out_file:
            html_text = self.to_html()
            out_file.write(html_text)
            out_file.close()


    def _get_header_text(self):
        """Create the HTML file segment before the charts.

        Returns:
            str: The HTML text to go before the charts.

        """

        header_text = '<!DOCTYPE html>\n'
        header_text += '<html>\n'
        header_text += '<head>\n'
        header_text += '<script src="http://ajax.googleapis.com/ajax/'\
                        'libs/jquery/1.8.2/jquery.min.js"></script>\n'
        header_text += '<script src="http://code.highcharts.com/highcharts.js"></script>\n'
        header_text += '</head>\n'
        header_text += '<body>\n'
        if self._heading_text is not None:
            header_text += '<h1 style="text-align:center;">%s</h1>\n'%self._heading_text

        return header_text

    @staticmethod
    def _get_footer_text():
        """Create the HTML text at the end of the file.

        Returns:
            str: The HTML text to go at the end after the charts.

        """

        footer_text = '\n\n</body>\n\n'
        footer_text = '</html>'

        return footer_text

    @staticmethod
    def _indent(num_spaces, text):
        """Prepend spaces to a string.

        Args:
            num_spaces (int): The number of spaces to prepent to the string.
            text (str): The text to be indented.

        Returns:
            str: The text with the spaces prepended.
        """

        return (' ' * num_spaces) + text


class Chart():
    """Class to construct and represent one chart."""
    def __init__(self):
        self._chart = {}
        self._set_defaults()
        self._width = 800
        self._height = 400

    def _set_defaults(self):
        self.set_credits()
        self.set_chart()
        self.set_title()
        self.set_subtitle()
        self.set_xaxis()
        self.set_yaxis()
        self.set_tooltip()
        self.set_plot_options()

    @property
    def width(self):
        """Get the defined width of the chart.
        Returns:
            int: The width of the chart.
        """

        return self._width

    @property
    def height(self):
        """Get the defined height of the chart.
        Returns:
            int: The height of the chart.
        """

        return self._height

    def set_width(self, width):
        """Set the width of the chart.

        Args:
            width (int): The width in pixels
        """

        self._width = width

    def set_height(self, height):
        """Set the height of the chart.

        Args:
            height (int): The height in pixels
        """

        self._height = height


    def set_chart(self, chart_type='line', zoom_type='x'):
        """Set the type and optionally the zoom type of this chart.

        Args:
            chart_type (str)
        """
        if chart_type is None:
            self._chart.pop('chart', None)
        self._chart['chart'] = {'type': chart_type, 'zoomType': zoom_type}

    def set_credits(self,
                    text='jrtools',
                    href='http://github.com/jrseti/jrtools'):
        """Set the credits.

        Args:
            text (str): The text element of the credit.
            href (str): THe URL of the credit text as a link.
        """

        self._chart['credits'] = {'text': text, 'href': href}

    def set_title(self, title='Chart Title'):
        """Set the title of the chart.

        Args:
            title (str): The title of the chart.
        """

        self._chart['title'] = {'text': title}

    def set_subtitle(self, subtitle=None):
        """Set the subtitle of the chart.

        Args:
            sustitle (str): The subtitle of the chart.
        """

        if subtitle is None:
            self._chart.pop('subtitle', None)
            return
        self._chart['subtitle'] = {'text': subtitle}

    def set_xaxis(self, axis_type='linear', text='Need to set X axis text'):
        """Set the x axis type and text.

        Args:
            axis_type (str): The type of the x axis.
            text (str): The x axis label.
        """

        self._chart['xAxis'] = dict()
        self._chart['xAxis']['type'] = axis_type
        self._chart['xAxis']['title'] = dict()
        self._chart['xAxis']['title']['text'] = text

    def set_yaxis(self, axis_type='linear', text='Need to set Y axis text'):
        """Set the y axis yype and text.

        Args:
            axis_type (str): The type of the y axis.
            text (str): The y axis label.
        """

        self._chart['yAxis'] = dict()
        self._chart['yAxis']['type'] = axis_type
        self._chart['yAxis']['title'] = dict()
        self._chart['yAxis']['title']['text'] = text

    def set_tooltip(self, tooltip_dict=None):
        """Set the tooltip definition.

        Args:
            tooltip_dict (dictionary): A dictionary defining the tooltip.
              This allows defining a custom tooltip to replace the default.
        """

        if tooltip_dict is None:
            self._chart.pop('tooltip', None)
            return
        self._chart['tooltip'] = tooltip_dict

    def set_plot_options(self, plot_options_dict=None):
        """Set the plotOptions.

        Args:
            plot_options_dictv(dictionary): A dictionary defining the plotOptions
            of the chart. This allows defining a custom plotOptions that will
            replace the default.
        """

        if plot_options_dict is None:
            self._chart.pop('plotOptions', None)
            return
        self._chart['plotOptions'] = plot_options_dict

    def add_series(self, series):
        """Add a series to this chart.

        Args:
            series (Series): An instance of the Series class.
        """

        series_list = self._chart.get('series', list())
        series_list.append(series.series)
        self._chart['series'] = series_list

    def to_json_string(self):
        """Get a string representation of the json representation of this
        chart.

        Returns:
            str: the string representation of this chart.
        Raises:
            Exception: If this chart does not contain a series.
        """

        if 'series' in self._chart:
            json_string = json.dumps(self._chart, indent=2)
            return json_string
        raise Exception(
            'The series has not been defined. Cannot create a valid chart.')


class Series:
    """Class to construct and represent one data series for a chart.

    Attributes:
        series (dict): The dictionary representation of the series.
    """

    def __init__(self, name, data, marker=None):
        """Constructor.

        Args:
            name (str): The name of the series. This name will be the name
                           as displayed in the chart.
            data (list): The data for this series.
            marker (dict): Optional marker definition for the series.

        """

        self._series = dict()
        self._series['name'] = name
        self._series['data'] = data
        if marker is not None:
            self._series['marker'] = marker

    @property
    def series(self):
        """Retrieve tis series

        Returns:
            dictionary: A dictionary definition of the series.

        """

        return self._series

    def set_series_type(self, series_type):
        """Set the type of the series. This is optional and used only when
        there are multiple series in a chart and they are of a different
        type.

        Args:
            value (str): The type of the series.

        """

        self._series['type'] = series_type

def main():
    """Function to test the main functionality of this module."""
    data = [[1, 1],
            [2, 2], [3, 3]]  #yapf: disable
    marker = {'marker': {'symbol': 'circle', 'radius': 0}}
    series = Series('test series', data, marker)
    chart = Chart()
    chart.set_title("My First Chart")
    chart.add_series(series)
    page = Page('Chart Test', 'This is my chart test')
    page.add_chart(chart)
    chart2 = copy.deepcopy(chart)
    chart2.set_width(800)
    chart2.set_height(400)
    page.add_chart(chart2)
    #print(page.to_html())


    page.to_file("testxx.html")

if __name__ == '__main__':
    main()
