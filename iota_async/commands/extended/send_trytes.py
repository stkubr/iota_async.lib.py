# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from typing import List, Optional

import filters as f

from iota_async import TransactionHash, TransactionTrytes, TryteString
from iota_async.commands import FilterCommand, RequestFilter
from iota_async.commands.core.attach_to_tangle import AttachToTangleCommand
from iota_async.commands.core.get_transactions_to_approve import \
    GetTransactionsToApproveCommand
from iota_async.commands.extended.broadcast_and_store import BroadcastAndStoreCommand
from iota_async.filters import Trytes

__all__ = [
    'SendTrytesCommand',
]


class SendTrytesCommand(FilterCommand):
    """
    Executes `sendTrytes` extended API command.

    See :py:meth:`iota_async.api.IotaApi.send_trytes` for more info.
    """
    command = 'sendTrytes'

    def get_request_filter(self):
        return SendTrytesRequestFilter()

    def get_response_filter(self):
        pass

    async def _execute(self, request):
        depth = request['depth']  # type: int
        min_weight_magnitude = request['minWeightMagnitude']  # type: int
        trytes = request['trytes']  # type: List[TryteString]
        reference = request['reference']  # type: Optional[TransactionHash]

        # Call ``getTransactionsToApprove`` to locate trunk and branch
        # transactions so that we can attach the bundle to the Tangle.
        gta_response = await GetTransactionsToApproveCommand(self.adapter)(
            depth=depth,
            reference=reference,
        )

        att_response = await AttachToTangleCommand(self.adapter)(
            branchTransaction=gta_response.get('branchTransaction'),
            trunkTransaction=gta_response.get('trunkTransaction'),

            minWeightMagnitude=min_weight_magnitude,
            trytes=trytes,
        )

        # ``trytes`` now have POW!
        trytes = att_response['trytes']

        await BroadcastAndStoreCommand(self.adapter)(trytes=trytes)

        return {
            'trytes': trytes,
        }


class SendTrytesRequestFilter(RequestFilter):
    def __init__(self):
        super(SendTrytesRequestFilter, self).__init__({
            'depth': f.Required | f.Type(int) | f.Min(1),

            'trytes':
                f.Required | f.Array | f.FilterRepeater(
                    f.Required | Trytes(TransactionTrytes),
                ),

            # Loosely-validated; testnet nodes require a different value
            # than mainnet.
            'minWeightMagnitude': f.Required | f.Type(int) | f.Min(1),

            'reference': Trytes(TransactionHash),
        },

            allow_missing_keys={
                'reference',
            })
