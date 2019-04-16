# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import filters as f

from iota_async import Bundle, TransactionHash
from iota_async.commands import FilterCommand, RequestFilter
from iota_async.commands.extended.get_bundles import GetBundlesCommand
from iota_async.commands.extended.send_trytes import SendTrytesCommand
from iota_async.filters import Trytes

__all__ = [
    'ReplayBundleCommand',
]


class ReplayBundleCommand(FilterCommand):
    """
    Executes ``replayBundle`` extended API command.

    See :py:meth:`iota_async.api.Iota.replay_bundle` for more information.
    """
    command = 'replayBundle'

    def get_request_filter(self):
        return ReplayBundleRequestFilter()

    def get_response_filter(self):
        pass

    async def _execute(self, request):
        depth = request['depth']  # type: int
        min_weight_magnitude = request['minWeightMagnitude']  # type: int
        transaction = request['transaction']  # type: TransactionHash

        gb_response = await GetBundlesCommand(self.adapter)(transaction=transaction)

        # Note that we only replay the first bundle returned by
        # ``getBundles``.
        bundle = gb_response['bundles'][0]  # type: Bundle

        return await SendTrytesCommand(self.adapter)(
            depth=depth,
            minWeightMagnitude=min_weight_magnitude,
            trytes=bundle.as_tryte_strings(),
        )


class ReplayBundleRequestFilter(RequestFilter):
    def __init__(self):
        super(ReplayBundleRequestFilter, self).__init__({
            'depth': f.Required | f.Type(int) | f.Min(1),
            'transaction': f.Required | Trytes(TransactionHash),

            # Loosely-validated; testnet nodes require a different value
            # than mainnet.
            'minWeightMagnitude': f.Required | f.Type(int) | f.Min(1),
        })
