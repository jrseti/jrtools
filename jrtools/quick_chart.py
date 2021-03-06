#!/usr/bin/env python3
# -*- coding: utf-8 -*-"

"""Creates a chart with your custom data. This charts is in the form of an HTML
   file and requires a browers to view.
   Highcharts (http://highcharts.com) is used as the javascript library to draw
   the chart.

   Example that creates the text of an HTML file containing a chart:

    import quick_chart as qc

    #Create a Chart object and set the title
    chart = qc.Chart()
    chart.set_title("My First Chart")

    #Create a data series
    data = [[1, 1], [2, 2], [3, 3]]
    marker = {'marker': {'symbol': 'circle', 'radius': 0}}
    series = qc.Series('test series', data, marker)

    #Add the series to the chart
    chart.add_series(series)

    #Create an HTML page object
    page = qc.Page('Chart Test')

    #Add the chart to the HTML page
    page.add_chart(chart)

    #Output the HTML to a file
    page.to_file("testxx.html")

"""
import os

import webbrowser
import tempfile
import time
import json


class Page():
    """Class to represent one HTML page in which the charts will reside. 
    
    Args:
        title_text (str): The title of this page. Will display in an h1 tag.

    """

    def __init__(self, title_text):

        self._title_text = title_text
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
                         'height:%dpx;"></div>\n' % (index,
                                                     chart.width, chart.height)
            html_text += Page._indent(2, "<script>\n")
            html_text += Page._indent(4, '$(function () {\n')

            for var_line in chart.get_series_js_var_statements():
                html_text += '%s\n' % Page._indent(6, var_line)

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
            filename (str): The path output filename.

        Raises:
            Exception: The result of opening and writing to the file.

        """

        with open(filename, 'w') as out_file:
            html_text = self.to_html()
            out_file.write(html_text)
            out_file.close()

    def display_in_browser(self, html_filename=None,
                           browser_type=None, verbose=True, delay=5):
        """Display this HTML page in a browser.

        The following steps are performed:

            1. The text of the HTML page containing the chart(s) is created.
            2. If the value of html_filename is None create and open a
               temporary file and write the HTML text to this file.
            3. If the value of html_filename is not None create the file
               and write the HTML text to this file.
            4. Using the webbrowser module load the HTML file in a browser.
            5. If html_filename was None and a temporary file was created,
               remove this file.

        Args:
            html_filename (str): The name of the html file to create for
               loading in a browser. If none, create a temporary file that
               is deleted after displayed.
            browser_type (str): Specify the brower type to display the file.
               If no value is provided the user's default browser is will
               used. See https://docs.python.org/2/library/webbrowser.html
               for a list of available browsers. safari, chrome, and firefox
               have been tested.
            verbose (bool): Prints some extra information that may be of
               interest to the user.
            delay (int): If html_filename is None and the browser loads
               delay temporary file, sleep this number of seconds before
               deleting the temporary file. If the delay is not long enough
               (depending on the speed of the bworser process on various
               computers) the file may be deleted before the browser gets
               around to displaying it. Defaults to 5 seconds.

        """

        # If html_filename is None, create the temporary file and load it.
        if html_filename is None:
            temporary_file = tempfile.NamedTemporaryFile(
                suffix='.html', delete=False, mode='w')
            html_filename = temporary_file.name
            self.to_file(html_filename)

            url = "file://%s" % html_filename
            webbrowser.get(browser_type).open(url, 1)
            if verbose is True:
                print('HTML file URL: %s' % url)
                print('Sleeping 5 seconds to allow browser to render the chart...')
            time.sleep(delay)
            os.unlink(html_filename)
            if verbose is True:
                print('%s deleted.' % html_filename)

            return

        # If html_filename is a filename (not None), load the file into a browser.
        self.to_file(html_filename)
        url = "file:///%s" % os.path.join(os.getcwd(), html_filename)
        webbrowser.get(browser_type).open(url, 1)
        if verbose is True:
            print('HTML file URL: %s' % url)

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
        if self._title_text is not None:
            header_text += '<h1 style="text-align:center;">%s</h1>\n' % self._title_text

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
    """Class to construct and represent one chart.  """

    def __init__(self):
        self._chart = {}
        self._series_instances_list = list()
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
        self._series_instances_list.append(series)
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
            json_string = Series.data_placeholder_replace(
                json_string, self._series_instances_list)
            return json_string
        raise Exception(
            'The series has not been defined. Cannot create a valid chart.')

    def get_series_js_var_statements(self):
        """Get a list of javascript var statements for the data in each

        Return:
            list(str): list of var statements for insertion into javascript.

        """

        if 'series' in self._chart:
            return Series.get_js_var_definitions(self._series_instances_list)
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
        self._series['data'] = '%s_placeholder' % name.replace(' ', '_')
        self._data = data
        if marker is not None:
            self._series['marker'] = marker

    def get_name(self):
        """Get the name of this series

        Return:
            str: the name of this series.

        """

        return self._series['name']

    def get_data_as_str(self):
        """Get the data, which is a list, as a string.

        Return:
            str: the data list as a string.

        """

        return str(self._data)

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

    def javascript_var_name(self):
        """Get the variable name for this variable in the javascript
        representation.

        Returns:
            str: the variable ae of this series to use in javascript.

        """

        var_name = '%s_data' % self._series['name'].replace(' ', '_')
        if var_name[0].isdigit() is True:
            var_name = '_' + var_name
        return var_name

    def to_javascript_var(self):
        """Convert this series to a var definition for Javascript.

        Example:
            if:
                self._series['name'] = 'xyz'
                and self._data = [[1,1],[2,2]]
            returns:
                'var series1_xyz = [[1,1],[2,2]];'

        Args:
            var_name_prefix (str): the string for the variable prefix.

        Returns:
            str: a var definition for this series' data.

        """

        return 'var %s = %s;' % (self.javascript_var_name(), self.get_data_as_str())

    @staticmethod
    def get_js_var_definitions(list_of_series):
        """Given a list of Series instances create list of var statements
        for javascript code insertion.

        Args:
            list_of_series (list): a list od Series instances.

        Returns:
            list(str): javascript var statements.

        """

        var_defs = list()
        for series in list_of_series:
            var_defs.append(series.to_javascript_var())

        return var_defs

    @staticmethod
    def data_placeholder_replace(json_string, list_of_series):
        """Given a list of Series instances substitute the placeholders in the
        json text.

        Args:
            json_string (str): a Chart json representation as a str.
            list_of_series (list): a list od Series instances.

        Returns:
            str: the json_string with the series popuplated with data = var name.

        """

        for series in list_of_series:
            placeholder_var_name = '%s_placeholder' % (
                series.get_name().replace(' ', '_'))
            json_string = json_string.replace(
                '"%s"' % placeholder_var_name, series.javascript_var_name())

        return json_string


def main():
    """Main function for testing."""

    data = [[1, 1], [2, 2], [3, 3]]
    data2 = [[1, 2], [2, 3], [3, 6]]
    marker = {'marker': {'symbol': 'circle', 'radius': 0}}
    series = Series('test series', data, marker)
    series2 = Series('test series 2', data2, marker)
    chart = Chart()
    chart.set_title("My First Chart")
    chart.add_series(series)
    chart.add_series(series2)
    page = Page('Chart Test')
    page.add_chart(chart)
    # page.add_chart(chart)
    print(page.to_html())

if __name__ == '__main__':
    main()
