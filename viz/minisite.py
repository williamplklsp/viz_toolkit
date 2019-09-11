import urllib.parse as urlparse
from urllib.parse import urlencode
from abc import ABC, abstractmethod
import IPython
import json
import pandas as pd


class MiniSiteChart(ABC):
    path = ""
    default_width = 950
    default_height = 500

    def __init__(self, host='http://localhost:5000'):
        self.host = host

    @staticmethod
    def _add_param(url, **params):
        url_parts = list(urlparse.urlparse(url))
        # scheme, netloc, url, params, query, fragment, _coerce_result
        url_parts[4] = urlencode(params, doseq=True)
        return urlparse.urlunparse(url_parts)

    @abstractmethod
    def _prep_param(self, data):
        pass

    def plot(self, data, width=None, height=None, **kwargs):
        width = self.default_width if width is None else width
        height = self.default_height if height is None else height
        params = self._prep_param(data)
        url = self._add_param(self.host + self.path, **params, **kwargs)
        return IPython.display.IFrame(url, height=height, width=width)


class Sankey(MiniSiteChart):
    """ Wrapped around basic example of multilayer sankey in
    https://developers.google.com/chart/interactive/docs/gallery/sankey
    """
    path = '/chart/sankey'
#     default_width=1000

    def _prep_param(self, data):
        out = {}
        out['from'] = list(data['from'].values)
        out['to'] = list(data['to'].values)
        out['values'] = list(data['values'].values)
        return out

    # def plot(self, data, width=None, height=None):
    #     """ Plot sankey with data and display in IPynb using IFrame(width, height)
    #         data is pd.DataFrame with 3 column
    #             from, to, value
    #     """
    #     super().plot(data, width, height)


class Sunburst(MiniSiteChart):
    """ Wrapped around basic example of multilayer sankey in
    https://developers.google.com/chart/interactive/docs/gallery/sankey
    """
    path = '/chart/sunburst'

    def _prep_param(self, data):
        def buildSequence(df):
            def get_parts(row):
                return json.dumps(
                    [s for s in row[row.index[:-1]].values if (not pd.isnull(s) and s)])
            return pd.DataFrame(zip(df.apply(get_parts, axis=1), df[df.columns[-1]]), columns=['sequences', 'values'])
        if not 'sequences' in data.columns:
            data = buildSequence(data)
        out = {}
        out['sequences'] = list(data['sequences'].values)
        out['values'] = list(data['values'].values)
        return out

    # def plot(self, data, width=None, height=None, **kwargs):
    #     """ Plot Sunburst with data and display in IPynb using IFrame(width, height)

    #         data {pd.DataFrame}
    #             1. pd.DataFrame with 2 column
    #                 Sequences: JSON string of list ['a', 'b', 'c'] representing the sequence
    #                 values: number, weight of the sequences
    #             or
    #             2. Multiple columns with values in last column
    #                 e.g.| c1 | c2 | c3 | c4 | v |
    #                     -------------------------
    #                     | 'a'|'b' | NAN| NAN| 3 |
    #                     | 'a'| 'b'| "c"| 'd'| 4 |
    #                     ...
    #                 it will be transformed to 1

    #         add_end {str, optional}: if specified, "[add_end]" will be added to each sequences
    #             e.g. ['Login', 'view', 'view', ..., "Drop out / end session"]
    #     """
    #     super().plot(data, width, height, **kwargs)


class SunburstZoomable(Sunburst):
    path = '/chart/zoom_sunburst'

    def _prep_param(self, data):
        def buildSequence(df):
            def get_parts(row):
                return json.dumps(
                    [s for s in row[row.index[:-1]].values if (not pd.isnull(s) and s)])
            return pd.DataFrame(zip(df.apply(get_parts, axis=1), df[df.columns[-1]]), columns=['sequences', 'values'])
        if not 'sequences' in data.columns:
            data = buildSequence(data)
        out = {}
        out['sequences'] = list(data['sequences'].values)
        out['values'] = list(data['values'].values)
        return out
