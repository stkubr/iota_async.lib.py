# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import filters as f

from iota_async import TransactionHash, TransactionTrytes
from iota_async.commands import FilterCommand, RequestFilter, ResponseFilter
from iota_async.filters import Trytes

__all__ = [
    'AttachToTangleCommand',
]


class AttachToTangleCommand(FilterCommand):
    """
    Executes ``attachToTangle`` command.

    See :py:meth:`iota_async.api.StrictIota.attach_to_tangle` for more info.
    """
    command = 'attachToTangle'

    def get_request_filter(self):
        return AttachToTangleRequestFilter()

    def get_response_filter(self):
        return AttachToTangleResponseFilter()


class AttachToTangleRequestFilter(RequestFilter):
    def __init__(self):
        super(AttachToTangleRequestFilter, self).__init__({
            'branchTransaction': f.Required | Trytes(TransactionHash),
            'trunkTransaction': f.Required | Trytes(TransactionHash),

            'trytes':
                f.Required |
                f.Array |
                f.FilterRepeater(
                    f.Required | Trytes(result_type=TransactionTrytes),
                ),

            # Loosely-validated; testnet nodes require a different value
            # than mainnet.
            'minWeightMagnitude': f.Required | f.Type(int) | f.Min(1),
        })


class AttachToTangleResponseFilter(ResponseFilter):
    def __init__(self):
        super(AttachToTangleResponseFilter, self).__init__({
            'trytes':
                f.FilterRepeater(
                    f.ByteString(encoding='ascii') |
                    Trytes(TransactionTrytes),
                ),
        })
