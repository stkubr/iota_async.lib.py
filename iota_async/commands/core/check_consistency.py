# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import filters as f

from iota_async import TransactionHash
from iota_async.commands import FilterCommand, RequestFilter
from iota_async.filters import Trytes

__all__ = [
    'CheckConsistencyCommand',
]


class CheckConsistencyCommand(FilterCommand):
    """
    Executes ``checkConsistency`` extended API command.

    See :py:meth:`iota_async.api.Iota.check_consistency` for more info.
    """
    command = 'checkConsistency'

    def get_request_filter(self):
        return CheckConsistencyRequestFilter()

    def get_response_filter(self):
        pass


class CheckConsistencyRequestFilter(RequestFilter):
    def __init__(self):
        super(CheckConsistencyRequestFilter, self).__init__({
            'tails':
                f.Required |
                f.Array |
                f.FilterRepeater(f.Required | Trytes(TransactionHash)),
        })
