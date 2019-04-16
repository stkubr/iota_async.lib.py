# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import filters as f

from iota_async.commands import FilterCommand, RequestFilter
from iota_async.filters import NodeUri

__all__ = [
    'AddNeighborsCommand',
]


class AddNeighborsCommand(FilterCommand):
    """
    Executes `addNeighbors` command.

    See :py:meth:`iota_async.api.StrictIota.add_neighbors`.
    """
    command = 'addNeighbors'

    def get_request_filter(self):
        return AddNeighborsRequestFilter()

    def get_response_filter(self):
        pass


class AddNeighborsRequestFilter(RequestFilter):
    def __init__(self):
        super(AddNeighborsRequestFilter, self).__init__({
            'uris':
                f.Required | f.Array | f.FilterRepeater(f.Required | NodeUri),
        })
